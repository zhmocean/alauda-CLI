OS = Linux

VERSION = 0.0.1

CURDIR = $(shell pwd)
SOURCEDIR = $(CURDIR)

ECHO = echo
RM = rm -rf
MKDIR = mkdir
FLAKE8 = flake8
PIP_INSTALL = pip install
RUN_UNITTESTS = python -m unittest clitests.parser_tests
INSTALL_CLI = ./local-install.sh

.PHONY: setup build test help

all: build test install

setup:
	$(PIP_INSTALL) $(FLAKE8)

build:
	$(FLAKE8) $(SOURCEDIR) --show-source --show-pep8 --statistics --count

test:
	$(RUN_UNITTESTS)

install:
	$(INSTALL_CLI)

help:
	@$(ECHO) "Targets:"
	@$(ECHO) "all     - setup, build and test"
	@$(ECHO) "setup   - set up prerequisites for build"
	@$(ECHO) "build   - perform static analysis"
	@$(ECHO) "test    - run unittests"