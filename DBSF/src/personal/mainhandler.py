import os
import subprocess
import sys
import sqlmap
from odathandler import *
from nmaphandler import *
from sqlhandler import *

commands = ""

print("1. Nmap\n", "2. SqlMap\n", "3. ODAT\n")

#user_input = ""

user_input = input("Enter Value : ")

print(user_input)

if user_input == "1":
    #commands = input("Please enter IP Address")
    commands = "nmap -h"
    run_nmap(commands)
elif user_input == "2":
    commands = "sqlmap -h"
    runsqlmap(commands)
elif user_input == "3":
    commands = ""
    run_odat(commands)
else:
    print("Please make sure you entered the correct number according to the tools")
    