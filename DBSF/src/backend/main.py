import os
import subprocess
import sqlmap
import sys

def runsqlmap(command):
    subprocess.run(command, shell=True)

#def testprint():
    #print("hello world")

runstring = "sqlmap -h"

runsqlmap(runstring)