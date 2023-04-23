import os
import subprocess
import sqlmap
import sys

def run_odat(command):
    subprocess.run(command, shell=True)

#runstring = "python3 odat.py -h"

#run_odat(runstring)