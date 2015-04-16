#!/bin/sh

sudo rm -r -f /Library/Python/2.7/site-packages/alaudacli
sudo rm /usr/bin/alauda
sudo cp -r alaudacli /Library/Python/2.7/site-packages/
sudo cp bin/alauda /usr/bin

