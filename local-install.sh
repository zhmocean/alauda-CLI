#!/bin/bash

sudo rm -r -f /usr/local/bin/alaudacli
sudo rm /usr/local/bin/alauda
sudo cp -r alaudacli /usr/local/bin
sudo cp bin/alauda /usr/local/bin

sudo rm /etc/bash_completion.d/alauda
sudo cp ./alauda /etc/bash_completion.d

. /etc/bash_completion.d/alauda

echo "Please re-login to finish the install!"
