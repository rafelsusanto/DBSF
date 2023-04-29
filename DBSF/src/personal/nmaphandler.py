import os
import subprocess
import sqlmap
import sys

def run_nmap(ip):
    CMD = "nmap -p 80 "+ ip
    op = subprocess.run(CMD, shell=True, stdout=subprocess.PIPE)
    print(op.stdout)

def test_ls():
    cmd = "ls"
    op = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    print(op.stdout)
#runstring = "nmap -h"

#run_nmap(runstring)

#nmap mau pake subprocess or pake library python-nmap?