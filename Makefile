help:
	@ echo 'Automated development tasks for padsniff.                                      '
	@ echo '                                                                               '
	@ echo 'Usage:                                                                         '
	@ echo '    make build         Build source and wheel distributions.                   '
	@ echo '    make build-source  Build only a source distribution.                       '
	@ echo '    make build-wheel   Build only a wheel distribution.                        '
	@ echo '    make clean         Clean build and cache files.                            '
	@ echo '    make clean-build   Clean only build files.                                 '
	@ echo '    make clean-cache   Clean only cache files.                                 '
	@ echo '    make develop       Install package in editable mode with dev dependencies. '
	@ echo '    make install       Install package with runtime dependencies.              '
	@ echo '    make publish       Build source and wheel distributions and upload to pypi.'
	@ echo '    make help          Show this message.                                      '
	@ echo '                                                                               '

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

.DEFAULT: help
.PHONY: help build build-source build-wheel clean clean-build clean-cache develop install publish test
