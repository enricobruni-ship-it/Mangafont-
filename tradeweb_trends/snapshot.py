"""Snapshot endpoint: Google Trends trending searches (US/UK/EU) checked for Tradeweb mentions.

Run:  python3 tradeweb_trends/snapshot.py   (serves on :8000)
GET /snapshot            -> JSON for all default countries
GET /snapshot?geo=US,GB  -> subset
GET /snapshot?term=foo   -> match a different keyword (default: tradeweb)
GET /interest            -> Google Trends interest (0-100) + related queries per country (needs pytrends)
GET /interest?geo=US,GB&timeframe=today 3-m&term=Tradeweb
"""
import time
import json
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import requests

GEOS = ["US", "GB", "DE", "FR", "IT", "ES", "NL", "IE"]
FEED = "https://trends.google.com/trending/rss?geo={geo}"
NS = {"ht": "https://trends.google.com/trending/rss"}


def fetch_geo(geo, term):
    out = {"geo": geo, "trending_count": 0, "matches": [], "top_trending": [], "error": None}
    try:
        r = requests.get(FEED.format(geo=geo), timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        items = ET.fromstring(r.content).findall(".//item")
    except Exception as e:  # network/parse errors reported per-country
        out["error"] = str(e)
        return out
    out["trending_count"] = len(items)
    for it in items:
        title = it.findtext("title", "")
        traffic = it.findtext("ht:approx_traffic", "", NS)
        news = [
            {"title": n.findtext("ht:news_item_title", "", NS),
             "source": n.findtext("ht:news_item_source", "", NS),
             "url": n.findtext("ht:news_item_url", "", NS)}
            for n in it.findall("ht:news_item", NS)
        ]
        if len(out["top_trending"]) < 5:
            out["top_trending"].append({"query": title, "traffic": traffic})
        haystack = " ".join([title, it.findtext("description", "")] + [n["title"] for n in news]).lower()
        if term in haystack:
            out["matches"].append({"query": title, "traffic": traffic, "news": news})
    return out


def snapshot(geos, term="tradeweb"):
    term = term.lower()
    with ThreadPoolExecutor(max_workers=len(geos)) as ex:
        results = list(ex.map(lambda g: fetch_geo(g, term), geos))
    return {
        "term": term,
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "total_matches": sum(len(r["matches"]) for r in results),
        "countries": results,
    }


def interest_geo(geo, term, timeframe):
    from pytrends.request import TrendReq
    out = {"geo": geo, "latest": None, "avg": None, "peak": None, "series": [],
           "top_queries": [], "rising_queries": [], "error": None}
    try:
        p = TrendReq(hl="en-US", tz=0, timeout=(5, 20))
        p.build_payload([term], geo=geo, timeframe=timeframe)
        df = p.interest_over_time()
        if not df.empty:
            vals = [int(v) for v in df[term]]
            out.update(latest=vals[-1], avg=round(sum(vals) / len(vals), 1), peak=max(vals),
                       series=[{"date": d.strftime("%Y-%m-%d"), "value": int(v)} for d, v in df[term].items()][-30:])
        rq = p.related_queries().get(term) or {}
        for key, name in (("top", "top_queries"), ("rising", "rising_queries")):
            frame = rq.get(key)
            if frame is not None:
                out[name] = frame.head(5).to_dict("records")
    except Exception as e:  # typically HTTP 429 when Google throttles
        out["error"] = str(e)
    return out


def interest(geos, term="Tradeweb", timeframe="today 3-m"):
    results = []
    for i, g in enumerate(geos):  # sequential + delay: Trends throttles parallel calls
        if i:
            time.sleep(1.5)
        r = interest_geo(g, term, timeframe)
        if r["error"] and "429" in r["error"]:  # one backoff retry
            time.sleep(8)
            r = interest_geo(g, term, timeframe)
        results.append(r)
    return {"term": term, "timeframe": timeframe,
            "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "note": "Values are relative 0-100 per country, not comparable across countries.",
            "countries": results}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        u = urlparse(self.path)
        if u.path not in ("/snapshot", "/interest"):
            self.send_error(404)
            return
        q = parse_qs(u.query)
        geos = [g.strip().upper() for g in q.get("geo", [",".join(GEOS)])[0].split(",") if g.strip()]
        if u.path == "/snapshot":
            data = snapshot(geos, q.get("term", ["tradeweb"])[0])
        else:
            data = interest(geos, q.get("term", ["Tradeweb"])[0], q.get("timeframe", ["today 3-m"])[0])
        body = json.dumps(data, indent=2).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    print("Serving http://localhost:8000/snapshot and /interest")
    ThreadingHTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
