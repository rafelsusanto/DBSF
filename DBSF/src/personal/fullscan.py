import os
import subprocess
import time
import sys
import threading
from .models import *
from .forms import *
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ODAT = 0
CTR_nmap = 0
CTR_hydra = 0
CTR_hydra_current = 0
CTR_sqlmap = 0

def run_fullscan(ip,db_id):
    thread = threading.Thread(target=run_script,args=(ip,db_id,))
    thread.setDaemon(True)
    thread.start()
    # thread.join()
    
def run_thread_hydra(ip, db_id, db_port, db_type):
    thread = threading.Thread(target=run_hydra,args=(ip,db_id,db_port, db_type,  ))
    thread.setDaemon(True)
    thread.start()

def run_hydra(ip,db_id, db_port, db_type):
    password_path = str(BASE_DIR) + "/static/files/password.txt"
    print(password_path)

    # hydra -l dvwa -P ./password 127.0.0.1 mysql
    CMD = "hydra -l dvwa -P "+password_path+" " + ip + " " + db_type + " -s " + db_port
    op = subprocess.run(CMD, shell=True, stdout=subprocess.PIPE)
    hasil = op.stdout
    hasil = hasil.decode('UTF-8')
    
    form = ScanResultForm({'ScanID': db_id, 'ScanType' : "2", 'Description': hasil})
    if form.is_valid():
        form.save()
    global CTR_hydra_current
    CTR_hydra_current+=1

def run_nmap(ip,db_id):
    CMD = "nmap -sC -sV "+ ip
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
        global CTR_hydra
        for c in container:
            if c.find('tcp open  mysql')!=-1:
                result += c
                result += '\n' 

                db_port = c.split('/')

                # jalanin threading buat hydra scanning
                CTR_hydra+=1

                run_thread_hydra(ip, db_id, db_port[0],"mysql")

            elif c.find('oracle')!=-1:
                result += c
                result += '\n' 
                ODAT = 1
                db_port = c.split('/')
                
                # jalanin threading buat hydra scanning
                CTR_hydra+=1

                run_thread_hydra(ip, db_id, db_port[0],"oracle")
        
        print(result)
        form = ScanResultForm({'ScanID': db_id, 'ScanType' : "1", 'Description': hasil})
        if form.is_valid():
            form.save()


    else:
        UPDATE = Scan.objects.get(pk=db_id)
        UPDATE.Status = "Failed"
        UPDATE.save()

        form = ScanResultForm({'ScanID': db_id, 'ScanType' : "9", 'Description': "Fail to run nmap!"})
        if form.is_valid():
            form.save()
    global CTR_nmap
    CTR_nmap=1
    
def run_thread_sql(packet_path,db_id):
    thread = threading.Thread(target=run_sqlmap,args=(packet_path,db_id,))
    thread.setDaemon(True)
    thread.start()

def run_sqlmap(packet_path,db_id):
    packet_path = str(packet_path)
    packet_path = str(BASE_DIR) + "/media/" + packet_path
    CMD = "sqlmap -r "+packet_path+" --batch --dump" 

    op = subprocess.run(CMD, shell=True, stdout=subprocess.PIPE)
    hasil = op.stdout
    hasil = hasil.decode('UTF-8')

    form = ScanResultForm({'ScanID': db_id, 'ScanType' : "3", 'Description': hasil})
    form.save()

    global CTR_sqlmap
    CTR_sqlmap=1

def run_script(ip,db_id):
    # run nmap
    run_nmap(ip,db_id)

    # run sqlmap
    TARGET = Scan.objects.get(pk=db_id)

    # cek kalo packetrequestnya tidak kosong
    if TARGET.PacketRequest != "":
        run_thread_sql(TARGET.PacketRequest,db_id)
    else:
        global CTR_sqlmap
        CTR_sqlmap=1
        

    # run odat


    # if statement cek kalo status nya fail atau ongoing
    i=0
    while i<=10:
        if CTR_nmap==1 and CTR_sqlmap==1 and CTR_hydra==CTR_hydra_current:
            i=11
            UPDATE = Scan.objects.get(pk=db_id)
            UPDATE.Status = "Done"
            UPDATE.save()
        else:
            time.sleep(5)
            