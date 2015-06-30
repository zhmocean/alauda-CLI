OS = Linux

VERSION = 0.2.4

CURDIR = $(shell pwd)
SOURCEDIR = $(CURDIR)

ECHO = echo
RM = rm -rf
MKDIR = mkdir
FLAKE8 = flake8
PIP_INSTALL = pip install
RUN_UNITTESTS = python -m unittest clitests.parser_tests
RUN_E2ETESTS = python -m unittest clitests.e2e_tests
INSTALL_CLI = ./local-install.sh
UNINSTALL_CLI = ./local-uninstall.sh

.PHONY: setup build ut test install uninstall help

all: build ut

setup:
	$(PIP_INSTALL) $(FLAKE8)

build:
	$(FLAKE8) $(SOURCEDIR) --show-source --show-pep8 --statistics --count

ut:
	$(RUN_UNITTESTS)

test:
	$(RUN_E2ETESTS)

install:
	$(INSTALL_CLI)

uninstall:
	$(UNINSTALL_CLI)

help:
	@$(ECHO) "Targets:"
	@$(ECHO) "all       - build, test and install"
	@$(ECHO) "setup     - set up prerequisites for build"
	@$(ECHO) "build     - perform static analysis"
	@$(ECHO) "ut        - run unittests"
	@$(ECHO) "test      - run e2e tests"
	@$(ECHO) "install   - install alaudacli locally"
	@$(ECHO) "uninstall - uninstall local alaudacli"
