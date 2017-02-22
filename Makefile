build: clean-build build-source build-wheel

build-source:
	python setup.py sdist

build-wheel:
	pip install wheel
	python setup.py bdist_wheel

clean: clean-build clean-cache

clean-build:
	rm -rf .eggs/ build/ dist/
	find . -name '*.egg' -exec rm -rf {} +
	find . -name '*.egg-info' -exec rm -rf {} +

clean-cache:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

develop:
	pip install -e .
	pip install -r dev-requirements.txt

install:
	pip install .

publish: build
	pip install twine
	twine upload --skip-existing dist/*

test:
	python setup.py test

.PHONY: build build-source build-wheel clean clean-build clean-cache develop install publish test
