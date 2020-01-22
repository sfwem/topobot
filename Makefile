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

md:
	pandoc README.rst -f rst -t markdown -o README.md

# Build Docker image
build: docker_build

run: docker_run

# Image and binary can be overidden with env vars.
DOCKER_IMAGE ?= ampledata/topobot

# Get the latest commit.
GIT_COMMIT = $(shell git rev-parse --short HEAD)

# Get the version number from the code
# FIXME(gba) There is probably a better way of doing this:
CODE_VERSION = $(shell grep ^__version__ setup.py |awk '{print $$3}'|sed s/\'//g)

# Find out if the working directory is clean
GIT_NOT_CLEAN_CHECK = $(shell git status --porcelain)
ifneq (x$(GIT_NOT_CLEAN_CHECK), x)
  DOCKER_TAG_SUFFIX = -dirty
endif

# If we're releasing to Docker Hub, and we're going to mark it with the latest tag,
#  it should exactly match a version release
ifeq ($(MAKECMDGOALS), release)

  # Use the version number as the release tag.
  DOCKER_TAG = $(CODE_VERSION)
  ifndef CODE_VERSION
	$(error You need to create a VERSION file to build a release)
  endif

  # See what commit is tagged to match the version
  VERSION_COMMIT = $(shell git rev-list $(CODE_VERSION) -n 1 | cut -c1-7)
  ifneq ($(VERSION_COMMIT), $(GIT_COMMIT))
	$(error echo You are trying to push a build based on commit $(GIT_COMMIT) but the tagged release version is $(VERSION_COMMIT))
  endif

  # Don't push to Docker Hub if this isn't a clean repo
  ifneq (x$(GIT_NOT_CLEAN_CHECK), x)
	$(error echo You are trying to release a build based on a dirty repo)
  endif

else
  # Add the commit ref for development builds. Mark as dirty if the working directory isn't clean
  DOCKER_TAG = $(CODE_VERSION)-$(GIT_COMMIT)$(DOCKER_TAG_SUFFIX)
endif

# Build the Docker container:
docker_build:
	# Build Docker image
	docker build \
		--build-arg BUILD_DATE=`date -u +"%Y-%m-%dT%H:%M:%SZ"` \
		--build-arg VERSION=$(CODE_VERSION) \
		--build-arg VCS_URL=`git config --get remote.origin.url` \
		--build-arg VCS_REF=$(GIT_COMMIT) \
		-t $(DOCKER_IMAGE):$(DOCKER_TAG) .

# Run the Docker container:
docker_run:
	docker run -it \
	    -p 8888:80 \
	    -e "MYSQL_ADMIN_PASS=changeme" \
		-e "MYSQL_USER_PASS=mesh-map_sql_user_password" \
		-v `pwd`/meshmap-mysql:/var/lib/mysql \
		-v `pwd`/user-settings.ini:/meshmap/scripts/user-settings.ini \
		$(DOCKER_IMAGE)

# Push the Docker container to Docker Hub (for local builds):
docker_push:
	# Tag image as latest
	docker tag $(DOCKER_IMAGE):$(DOCKER_TAG) $(DOCKER_IMAGE):latest

	# Push to DockerHub
	docker push $(DOCKER_IMAGE):$(DOCKER_TAG)
	docker push $(DOCKER_IMAGE):latest

output:
	@echo Docker Image: $(DOCKER_IMAGE):$(DOCKER_TAG)

date:
	@echo $(shell date)
