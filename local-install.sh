#!/bin/sh

sudo rm -r -f /usr/local/bin/alaudacli
sudo rm /usr/local/bin/alauda
sudo cp -r alaudacli /usr/local/bin
sudo cp bin/alauda /usr/local/bin

