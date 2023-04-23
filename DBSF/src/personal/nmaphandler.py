import os
import subprocess
import sqlmap
import sys

def run_nmap(command):
    subprocess.run(command, shell=True)

#runstring = "nmap -h"

#run_nmap(runstring)

#nmap mau pake subprocess or pake library python-nmap?