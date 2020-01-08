# Makefile for TopoBot.
#
# Source:: https://github.com/ampledata/topobot
# Author:: Greg Albrecht W2GMD <oss@undef.net>
# Copyright:: Copyright 2020 Greg Albrecht
# License:: Apache License, Version 2.0
#


.DEFAULT_GOAL := all


all: develop

install_requirements:
	pip install -r requirements.txt

install_requirements_tests:
	pip install -r requirements.txt

develop: remember
	python setup.py develop

install: remember
	python setup.py install

uninstall:
	pip uninstall -y topobot

reinstall: uninstall install

remember:
	@echo
	@echo "Hello from the Makefile..."
	@echo "Don't forget to run: 'make install_requirements'"
	@echo

remember_tests:
	@echo
	@echo "Hello from the Makefile..."
	@echo "Don't forget to run: 'make install_requirements_tests'"
	@echo

clean:
	@rm -rf *.egg* build dist *.py[oc] */*.py[co] cover doctest_pypi.cfg \
		nosetests.xml pylint.log output.xml flake8.log tests.log \
		test-result.xml htmlcov fab.log .coverage

publish:
	python setup.py register sdist upload

nosetests: remember
	python setup.py nosetests

pep8: remember
	flake8 --max-complexity 12 --exit-zero *.py topobot/*.py tests/*.py

flake8: pep8

lint: remember
	pylint --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" \
		-r n *.py topobot/*.py tests/*.py || exit 0

pylint: lint

mypy: remember_tests
	mypy --ignore-missing-imports --strict .

test: lint pep8 nosetests
