
all: dist/*.whl


python_sources := $(wildcard owul/**/*.py) $(wildcard owul/*.py)

dist/%.whl: Makefile pyproject.toml README.md $(python_sources)
	python -m hatchling build -t wheel