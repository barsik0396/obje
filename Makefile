all: build

build:
	nuitka --standalone --follow-imports --onefile main.py --output-dir=dist >/dev/null 2>&1

clean:
	rm -rf dist/
