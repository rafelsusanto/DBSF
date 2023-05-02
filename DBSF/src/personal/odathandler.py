import os
import subprocess
import sqlmap
import sys

path = "python3 ./backend/odat/"

def run_odat(command):
    subprocess.run(path + command, shell=True)

#runstring = "python3 odat.py -h"