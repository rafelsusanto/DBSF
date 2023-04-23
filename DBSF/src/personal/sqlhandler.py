import os
import subprocess
import sqlmap
import sys

def runsqlmap(command):
    subprocess.run(command, shell=True)

#runstring = "sqlmap -h"

#runsqlmap(runstring)