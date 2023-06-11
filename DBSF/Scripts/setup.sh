#!/bin/bash

source ../env/bin/activate

sudo apt-get update -y

sudo apt-get install -y nmap sqlmap hydra python3-scapy odat default-libmysqlclient-dev
sudo pip3 install colorlog termcolor pycrypto passlib python-libnmap libpython3-dev alien python3-pip cx_Oracle
sudo pip3 install argcomplete && sudo activate-global-python-argcomplete
python3 -m pip install -r ../src/requirements.txt
git submodule update --init --recursive