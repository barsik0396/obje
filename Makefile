all: build

build:
	nuitka --standalone --follow-imports --onefile main.py --output-dir=dist

clean:
	rm -rf dist/
