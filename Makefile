.PHONY: install test lint demo
install:
	python -m pip install -e '.[dev]'
test:
	python -m pytest -q
lint:
	ruff check src tests examples
demo:
	python -m canprod fit --input examples/synthetic_production.csv --base-year 2012 --outdir outputs/demo --plot
