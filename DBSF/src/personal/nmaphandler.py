import os
import subprocess
import sqlmap
import sys
import threading

def run_thread():
    proc = run_nmap()
    proc.save()
    thread = threading.thread(target=start_nmap,args=[proc.id])
    thread.setDaemon(True)
    thread.start()
    #set a return value

def run_nmap(ip):
    CMD = "nmap -p 80 "+ ip
    op = subprocess.run(CMD, shell=True, stdout=subprocess.PIPE)
    print(op.stdout)

def test_ls():
    cmd = "ls"
    op = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    print(op.stdout)

def start_nmap():
    #get process id from db

    #save result
    #set done flag as true
    #save
#runstring = "nmap -h"

#run_nmap(runstring)

#nmap mau pake subprocess or pake library python-nmap?