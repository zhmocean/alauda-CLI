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
UNINSTALL_CLI = ./local-uninstall.sh

.PHONY: setup build test install uninstall help

all: build test

setup:
	$(PIP_INSTALL) $(FLAKE8)

build:
	$(FLAKE8) $(SOURCEDIR) --show-source --show-pep8 --statistics --count

test:
	$(RUN_UNITTESTS)

install:
	$(INSTALL_CLI)

uninstall:
	$(UNINSTALL_CLI)

help:
	@$(ECHO) "Targets:"
	@$(ECHO) "all       - build, test and install"
	@$(ECHO) "setup     - set up prerequisites for build"
	@$(ECHO) "build     - perform static analysis"
	@$(ECHO) "test      - run unittests"
	@$(ECHO) "install   - install alaudacli locally"
	@$(ECHO) "uninstall - uninstall local alaudacli"