#!/bin/sh

/usr/local/bin/autopep8 --verbose --recursive --exclude migrations,settings_docker.py --max-line-length 160 --in-place --aggressive --aggressive .;


