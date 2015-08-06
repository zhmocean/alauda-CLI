#!/bin/bash

sudo rm -r -f /usr/local/bin/alaudacli
sudo rm /usr/local/bin/alauda
sudo cp -r alaudacli /usr/local/bin
sudo cp bin/alauda /usr/local/bin


sys=`uname -s`

if [ $sys == "Linux" ]
then
sudo rm /etc/bash_completion.d/alauda
sudo cp ./alauda /etc/bash_completion.d
. /etc/bash_completion.d/alauda
else
sudo rm /usr/local/etc/bash_completion.d/alauda
sudo cp ./alauda /usr/local/etc/bash_completion.d/
echo ". /usr/local/etc/bash_completion.d/alauda" >> ~/.bash_profile

fi

