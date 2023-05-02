#!/bin/bash

sudo apt-get update -y

sudo apt-get install -y nmap
sudo apt-get install -y sqlmap
sudo apt-get install -y hydra
sudo apt-get install -y python3-scapy
sudo pip3 install colorlog termcolor pycrypto passlib python-libnmap libaio1 python3-dev alien python3-pip cx_Oracle
sudo pip3 install argcomplete && sudo activate-global-python-argcomplete

python3 -m pip install -r ../src/requirements.txt