"""Rebuild the download: specimen PDFs and Mangafont.zip, from the
fonts currently in build/.

These used to be made by hand, which is exactly how they went stale --
build/Mangafont.zip sat three commits behind the fonts beside it, so
anyone downloading the zip installed an older face than the repository
advertised.  `make dist` now regenerates both from whatever `make font`
last produced.
"""
import base64, glob, os, shutil, subprocess, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, "build")
SPEC = os.path.join(ROOT, "specimen")

# The shipped families, and the two candidate cuts the comic specimen
# sets its comparison in (weights.CANDIDATES, built by directions.py).
FACES = [
    ("Mangafont",        "Mangafont-Regular.woff2",      "400"),
    ("Mangafont",        "Mangafont-Bold.woff2",         "700"),
    ("Mangafont Text",   "MangafontText-Regular.woff2",  "400"),
    ("Mangafont Text",   "MangafontText-Bold.woff2",     "700"),
    ("Mangafont Comic",  "MangafontComic-Regular.woff2", "400"),
    ("Mangafont Brush",  "MangafontBrush.woff2",         "400"),
    ("Mangafont Block",  "MangafontBlock.woff2",         "400"),
]


def _chromium():
    for p in sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome")):
        return p
    for p in ("/usr/bin/chromium", "/usr/bin/chromium-browser",
              "/usr/bin/google-chrome"):
        if os.path.exists(p):
            return p
    return None


def faces_css(tmp):
    out = []
    for family, fname, weight in FACES:
        path = os.path.join(BUILD, fname)
        if not os.path.exists(path):
            path = os.path.join(tmp, fname)
        if not os.path.exists(path):
            print("   ! missing %s, skipping that face" % fname)
            continue
        data = base64.b64encode(open(path, "rb").read()).decode()
        out.append('@font-face{font-family:"%s";font-weight:%s;font-style:normal;'
                   'font-display:block;src:url("data:font/woff2;base64,%s") '
                   'format("woff2");}' % (family, weight, data))
    return "\n".join(out)


def pdf(name, out_name, css, exe, tmp):
    src = os.path.join(SPEC, name)
    html = open(src).read()
    if "__FACES__" not in html:
        print("   ! %s has no __FACES__ slot, skipping" % name)
        return False
    page = os.path.join(tmp, name)
    open(page, "w").write(html.replace("__FACES__", css))
    out = os.path.join(BUILD, out_name)
    subprocess.run([exe, "--headless", "--disable-gpu", "--no-sandbox",
                    "--no-pdf-header-footer", "--print-to-pdf=" + out,
                    "file://" + page],
                   check=True, capture_output=True, timeout=180)
    print("   %-34s %d KB" % (out_name, os.path.getsize(out) // 1024))
    return True


def make_zip():
    out = os.path.join(BUILD, "Mangafont.zip")
    groups = [("install-these (TTF)", "*.ttf"),
              ("design-apps (OTF)", "*.otf"),
              ("web (WOFF2)", "*.woff2")]
    shipped = ("Mangafont-Regular", "Mangafont-Bold", "MangafontText-Regular",
               "MangafontText-Bold", "MangafontComic-Regular")
    n = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for folder, pat in groups:
            for f in sorted(glob.glob(os.path.join(BUILD, pat))):
                if os.path.splitext(os.path.basename(f))[0] not in shipped:
                    continue
                z.write(f, "Mangafont/%s/%s" % (folder, os.path.basename(f)))
                n += 1
        for extra, arc in (("OFL.txt", "Mangafont/OFL.txt"),
                           ("packaging/INSTALL.txt", "Mangafont/INSTALL.txt")):
            p = os.path.join(ROOT, extra)
            if os.path.exists(p):
                z.write(p, arc)
        for p in sorted(glob.glob(os.path.join(BUILD, "*-Specimen.pdf"))):
            z.write(p, "Mangafont/" + os.path.basename(p))
    print("   %-34s %d KB  (%d font files)"
          % ("Mangafont.zip", os.path.getsize(out) // 1024, n))


def main():
    tmp = os.path.join(BUILD, "_pkg")
    os.makedirs(tmp, exist_ok=True)
    try:
        # The comic specimen sets two candidate cuts that build.py does
        # not emit, so ask directions.py for them first.
        sys.path.insert(0, os.path.join(ROOT, "src"))
        sys.path.insert(0, os.path.join(ROOT, "tools"))
        try:
            import directions
            directions.main(tmp)
        except Exception as e:                      # not fatal: those two
            print("   ! candidate cuts unavailable (%s)" % e)

        exe = _chromium()
        if exe is None:
            print("   ! no chromium found, skipping the PDFs")
        else:
            css = faces_css(tmp)
            pdf("document.html", "Mangafont-Specimen.pdf", css, exe, tmp)
            pdf("comic.html", "MangafontComic-Specimen.pdf", css, exe, tmp)
        make_zip()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
