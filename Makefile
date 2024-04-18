all:
	echo "Please check the Makefile for available targets"

VERSION := '0.1'
TAG := 'egenix-advanced-match-parsing-$(VERSION)'

### Prepare the virtual env

install-pyrun:
	install-pyrun pyenv

install-venv:
	python3.11 -m venv pyenv

packages:
	pip install -r requirements.txt

dev-packages:   packages
	pip install -r requirements-dev.txt

update-packages:
	pip install -U -r requirements-base.txt

### Build

clean:
	find . \( -name '*~' -or -name '*.bak' \) -exec rm {} ';'

distclean:	clean
	rm -rf build dist *.egg-info __pycache__

create-dist:	clean
	echo "Building distributions for version $(VERSION)"
	python3 setup.py sdist bdist_wheel

tag-release:
	git tag -a $(TAG) -m "Release $(VERSION)"
	git push origin --tags

test-upload:
	python3 -m twine upload -r testpypi dist/*$(VERSION).tar.gz
	python3 -m twine upload -r testpypi dist/*$(VERSION)-py*.whl

prod-upload:
	python3 -m twine upload dist/*$(VERSION).tar.gz
	python3 -m twine upload dist/*$(VERSION)-py*.whl
	cp dist/*$(VERSION).tar.gz ~/projects/archives

### Run

run:
	python3 -m bench_match
