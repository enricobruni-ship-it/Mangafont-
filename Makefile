PY ?= python3
export PYTHONPATH = src

all: font

font:
	$(PY) -m mangafont.build

proof:
	$(PY) tools/preview.py build/proof.png all

check: font
	$(PY) tools/render_ttf.py build/Mangafont-Regular.ttf \
		"Pack my box with five dozen liquor jugs" build/pangram.png 78

specimen: font
	@echo "open specimen/index.html"

# The specimen PDFs and the download zip.  Made by hand once, which is
# how they ended up three commits behind the fonts beside them.
dist: font
	$(PY) tools/package.py

clean:
	rm -rf build/*.ttf build/*.woff2 build/*.png
	find src tools -name '__pycache__' -type d -exec rm -rf {} +

.PHONY: all font proof check specimen dist clean
