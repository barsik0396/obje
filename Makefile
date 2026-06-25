all: build

build:
	nuitka --standalone --onefile main.py --output-dir=dist

clean:
	rm -rf dist/
