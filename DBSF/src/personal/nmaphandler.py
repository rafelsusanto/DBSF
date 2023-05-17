import os
import subprocess
import sys
import threading
from .models import *
from .forms import *
from .hydrahandler import *


def run_thread_nmap(ip,db_id):
    thread = threading.Thread(target=run_script,args=(ip,db_id,))
    thread.setDaemon(True)
    thread.start()
    thread.join()
    
    # if statement cek kalo status nya fail atau ongoing
    UPDATE = Scan.objects.get(pk=db_id)
    UPDATE.Status = "Done"
    UPDATE.save()

def run_nmap(ip,db_id):
    CMD = "nmap -sC -sV "+ ip
    print(CMD)
    # CMD = "nmap -p 80 "+ ip
    op = subprocess.run(CMD, shell=True, stdout=subprocess.PIPE)
    hasil = op.stdout
    hasil = hasil.decode('UTF-8')

    # Checking if host is up
    if hasil.find("Host is up"):
        container = hasil.split('\n')
        db_type = 0
        # check if port is mysql / oracle 
        result = ""
        for c in container:
            if c.find('tcp open  mysql')!=-1:
                result += c
                result += '\n' 

                db_port = c.split('/')

                # jalanin threading buat hydra scanning
                run_thread_hydra(ip, db_id, db_port[0],"mysql")

            elif c.find('oracle')!=-1:
                result += c
                result += '\n' 

                db_port = c.split('/')
                
                # jalanin threading buat hydra scanning
                run_thread_hydra(ip, db_id, db_port[0],"oracle")
        
        print(result)
        form = ScanResultForm({'ScanID': db_id, 'ScanType' : "1", 'Description': hasil})
        form.save()


    else:
        UPDATE = Scan.objects.get(pk=db_id)
        UPDATE.Status = "Failed"
        UPDATE.save()

        form = ScanResultForm({'ScanID': db_id, 'ScanType' : "9", 'Description': "Fail to run nmap!"})
        form.save()
    

def run_script(ip,db_id):
    # run nmap
    run_nmap(ip,db_id)

    # run sqlmap


    # run odat
    


def test_ls():
    cmd = "ls"
    op = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    print(op.stdout)
