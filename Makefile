VERSION=$(shell python3 -c "import betterbib; print(betterbib.__version__)")

default:
	@echo "\"make publish\"?"

tag:
	# Make sure we're on the master branch
	@if [ "$(shell git rev-parse --abbrev-ref HEAD)" != "master" ]; then exit 1; fi
	@echo "Tagging v$(VERSION)..."
	git tag v$(VERSION)
	git push --tags

upload: setup.py
	@if [ "$(shell git rev-parse --abbrev-ref HEAD)" != "master" ]; then exit 1; fi
	rm -f dist/*
	python3 setup.py sdist
	python3 setup.py bdist_wheel --universal
	twine upload dist/*

publish: tag upload

clean:
	@find . | grep -E "(__pycache__|\.pyc|\.pyo$\)" | xargs rm -rf
	@rm -rf *.egg-info/ build/ dist/

lint:
	black --check setup.py betterbib/ test/ tools/betterbib-dedup-doi tools/betterbib-doi2bibtex tools/betterbib-format tools/betterbib-journal-abbrev tools/betterbib-sync tools/bibitems2bibtex
	flake8 setup.py betterbib/ test/ tools/betterbib-dedup-doi tools/betterbib-doi2bibtex tools/betterbib-format tools/betterbib-journal-abbrev tools/betterbib-sync tools/bibitems2bibtex
