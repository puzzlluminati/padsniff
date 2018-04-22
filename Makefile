PACKAGE := padsniff
VERSION ?= $(shell git describe --tags --abbrev=0)
REVISION ?= $(shell git rev-parse HEAD)

# setuptools normalizes the version (e.g., v1.2.3-beta -> 1.2.3b0)
# the normalized version is what our files will be named after
CLEANVERSION := $(shell python -c "from pkg_resources.extern.packaging.version import Version; print(Version('$(VERSION)'))")

SDIST := "dist/$(PACKAGE)-$(CLEANVERSION).tar.gz"
WHEEL := "dist/$(PACKAGE)-$(CLEANVERSION)-py3-none-any.whl"
INSTALLEDPACKAGES := $(shell pip list)

.DEFAULT: help
.PHONY: help
help:
	@ echo 'Automated development tasks for padsniff.                                      '
	@ echo '                                                                               '
	@ echo 'Usage:                                                                         '
	@ echo '    make clean         Clean build and cache files.                            '
	@ echo '    make develop       Install package in editable mode with dev dependencies. '
	@ echo '    make install       Install package with runtime dependencies.              '
	@ echo '    make package       Build source and wheel distributions.                   '
	@ echo '    make publish       Build source and wheel distributions and upload to pypi.'
	@ echo '    make sdist         Build source distribution.                              '
	@ echo '    make test          Run unit tests.                                         '
	@ echo '    make update-meta   Update padsniff/meta.py with current git revision.      '
	@ echo '    make wheel         Build wheel distribution.                               '
	@ echo '    make help          Show this message.                                      '
	@ echo '                                                                               '

.PHONY: clean
clean:
	rm -vrf *.egg-info .eggs build dist
	find . -name '*.pyc' -o -name '*.pyo' -o -name '__pycache__' -exec rm -vf {} +

.PHONY: develop
develop:
	pip install -e .
	pip install -r dev-requirements.txt

.PHONY: install
install:
	pip install .

.PHONY: package
package: update-meta sdist wheel

.PHONY: publish
publish: package
ifeq (,$(findstring twine,$(INSTALLEDPACKAGES)))
	$(error the twine library is required to upload package distributions, install it with "pip install twine")
else
	twine upload $(SDIST) $(WHEEL)
endif

.PHONY: sdist
sdist: $(SDIST)

.PHONY: test
test:
	python setup.py test

.PHONY: update-meta
update-meta:
	sed -i.bak -e "s,\(version =\) '\(.*\)',\1 '$(CLEANVERSION)'," -e "s,\(revision =\) '\(.*\)',\1 '$(REVISION)'," padsniff/meta.py

.PHONY: wheel
wheel: $(WHEEL)

$(SDIST):
	python setup.py sdist

$(WHEEL):
ifeq (,$(findstring wheel,$(INSTALLEDPACKAGES)))
	$(error the wheel library is required to build a binary wheel, install it with "pip install wheel")
else
	python setup.py bdist_wheel
endif
