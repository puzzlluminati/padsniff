.PHONY: build

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
	pip install -r requirements.txt
	pip install -r dev-requirements.txt
	pip install -e .

install:
	pip install -r requirements.txt
	python setup.py install

publish: build
	pip install twine
	twine upload dist/* -u $(PYPI_USERNAME) -p $(PYPI_PASSWORD) -r $(PYPI_REPOSITORY)

test:
	python setup.py test
