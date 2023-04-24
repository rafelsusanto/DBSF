#!/bin/bash

sudo apt-get update

sudo apt-get install -y nmap
sudo apt-get install -y odat
sudo apt-get install -y sqlmap

python3 -m pip install -r ../src/requirements.txt