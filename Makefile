
all: $(dist)/%.whl

$(dist)/%.whl: Makefile pyproject.toml README.md $(wildcard owul/*.py)
	python -m hatchling build -t wheel