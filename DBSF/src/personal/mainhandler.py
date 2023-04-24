import os
import subprocess
import sys
import sqlmap
from odathandler import *
from nmaphandler import *
from sqlhandler import *

commands = ""

print("1. Nmap\n", "2. SqlMap\n", "3. ODAT\n")

user_input = input("Enter Value : ")

if user_input == 1:
    commands = input("Please enter IP Address")
    run_nmap()
elif user_input == 2:
    commands = input("Please enter IP Address")
    runsqlmap()
elif user_input == 3:
    commands = input("Please enter IP Address")
    run_odat()
else:
    print("Please make sure you entered the correct number according to the tools")
    