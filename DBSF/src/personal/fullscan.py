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
CTR=0
CTR_current=0
CTR_nmap = 0
CTR_hydra = 0
CTR_hydra_current = 0
CTR_tns = 0
CTR_tns_current = 0
CTR_sqlmap = 0

def run_fullscan(ip,db_id):
    thread = threading.Thread(target=run_script,args=(ip,db_id,))
    thread.setDaemon(True)
    thread.start()
    # thread.join()
    
def run_thread_hydra(ip, db_id, db_port, db_type):
    global CTR_hydra
    CTR_hydra+=1
    thread = threading.Thread(target=run_hydra,args=(ip,db_id,db_port, db_type,  ))
    thread.setDaemon(True)
    thread.start()

def run_hydra(ip,db_id, db_port, db_type):
    password_path = str(BASE_DIR) + "/static/files/password.txt"
    username_path = str(BASE_DIR) + "/static/files/username.txt"
    sid_list_path = str(BASE_DIR) + "/static/files/sid.txt"
    print(password_path)

    # hydra -l dvwa -P ./password 127.0.0.1 mysql
    if db_type=="oracle":
        CMD = "hydra -L " + sid_list_path + " " + ip + " oracle-sid -s "+ db_port
    else:
        CMD = "hydra -L "+ username_path + " -P "+password_path+" " + ip + " " + db_type + " -s " + db_port
    print(CMD)
    op = subprocess.run(CMD, shell=True, stdout=subprocess.PIPE)
    hasil = op.stdout
    hasil = hasil.decode('UTF-8')
    print(f"hasil hydra {hasil}")
    container = hasil.split('\n')
    
    if db_type=="oracle":
        # cek sid ketemu ga
        sidList = "" + str(db_port)
        for c in container:
            if c.find("login: ")!=-1:
                sid = c.split('login: ')[1]
                sidList = sidList + "\n" + "- "+ sid
                run_thread_tns(ip, db_id, db_port, sid)
        print(f"sidList = {sidList}")
        form = ScanResultForm({'ScanID': db_id, 'ScanType' : "4", 'Description': sidList})

    elif db_type=="mysql":
        credentialList = "" + str(db_port)
        for c in container:
            if c.find("login: ")!=-1:
                credential = c.split("login: ")
                credential = credential[1]
                credential = credential.replace(" ","")
                credential = credential.split("password:")
                credentialList = credentialList + "\n" + credential[0] + "###" + credential[1]
        print(f"credentialList = {credentialList}")
        form = ScanResultForm({'ScanID': db_id, 'ScanType' : "2", 'Description': credentialList})
                
        

    if form.is_valid():
        form.save()
    global CTR_hydra_current
    CTR_hydra_current+=1

def run_thread_tns(ip, db_id, db_port,sid):
    global CTR
    CTR+=1
    thread = threading.Thread(target=run_tns,args=(ip,db_id,db_port,sid,   ))
    thread.setDaemon(True)
    thread.start()

def run_tns(ip, db_id, db_port,sid):
    odat_path = str(BASE_DIR) + "/personal/backend/odat/odat.py"
    CMD = "python3 "+odat_path+" tnspoison -s "+ip+" -p "+db_port+" -d "+sid+" --test-module"
    op = subprocess.run(CMD, shell=True, stdout=subprocess.PIPE)
    hasil = op.stdout
    hasil = hasil.decode('UTF-8')
    hasil = str(db_port)+'\n'+hasil
    form = ScanResultForm({'ScanID': db_id, 'ScanType' : "6", 'Description': hasil})
    if form.is_valid():
        form.save()

    global CTR_current
    CTR_current+=1

def run_thread_va(ip, db_id, db_port):
    global CTR
    CTR+=1
    thread = threading.Thread(target=run_va,args=(ip,db_id,db_port,   ))
    thread.setDaemon(True)
    thread.start()

def run_va(ip, db_id, db_port):
    CMD = "nmap -p "+db_port+" -sV --script vulners "+ip
    op = subprocess.run(CMD, shell=True, stdout=subprocess.PIPE)
    hasil = op.stdout
    hasil = hasil.decode('UTF-8')
    
    cleanData = hasil.split('VERSION')
    cleanData = cleanData[1]
    cleanData = cleanData.split('Service detection performed.')
    cleanData = cleanData[0]
    print(f"hasil va : {cleanData}")
    form = ScanResultForm({'ScanID': db_id, 'ScanType' : "5", 'Description': cleanData})
    if form.is_valid():
        form.save()

    global CTR_current
    CTR_current+=1
    


def run_nmap(ip,db_id, cmd):
    CMD = cmd + ip
    # CMD = "nmap -p 80 "+ ip
    op = subprocess.run(CMD, shell=True, stdout=subprocess.PIPE)
    hasil = op.stdout
    hasil = hasil.decode('UTF-8')

    # Checking if host is up
    if hasil.find("Host is up")!=-1:
        container = hasil.split('\n')
        db_type = 0
        # check if port is mysql / oracle 
        result = ""
        
        for c in container:
            if c.find('tcp open  mysql')!=-1 or c.find('tcp  open  mysql')!=-1 or c.find('tcp   open  mysql')!=-1 or c.find('tcp open     mysql')!=-1 or c.find('tcp  open     mysql')!=-1 or c.find('tcp   open     mysql')!=-1:
                result += c
                result += '\n' 

                db_port = c.split('/')

                # jalanin threading buat scanning
                run_thread_hydra(ip, db_id, db_port[0],"mysql")
                run_thread_va(ip,db_id,db_port[0])
            elif c.find('tcp open  oracle')!=-1 or c.find('tcp  open  oracle')!=-1 or c.find('tcp   open  oracle')!=-1 or c.find('tcp open     oracle')!=-1 or c.find('tcp  open     oracle')!=-1 or c.find('tcp   open     oracle')!=-1:
                result += c
                result += '\n' 
                ODAT = 1
                db_port = c.split('/')
                
                # jalanin threading buat scanning
                run_thread_hydra(ip, db_id, db_port[0],"oracle")
                run_thread_va(ip,db_id,db_port[0])
            elif c.find('tcp open')!=-1 or c.find('tcp  open')!=-1 or c.find('tcp   open')!=-1 or c.find('tcp filtered')!=-1 or c.find('tcp  filtered')!=-1 or c.find('tcp   filtered')!=-1:
                result += c
                result += '\n' 
        # print(result)
        form = ScanResultForm({'ScanID': db_id, 'ScanType' : "1", 'Description': result})
        if form.is_valid():
            form.save()
    elif hasil.find("try -Pn")!=-1:
        run_nmap(ip,db_id, "nmap -sV -Pn ")
    else:
        print("berhasil ke else")
        UPDATE = Scan.objects.get(pk=db_id)
        UPDATE.Status = "Failed"
        UPDATE.save()

        # form = ScanResultForm({'ScanID': db_id, 'ScanType' : "9", 'Description': "Fail to run nmap!"})
        # if form.is_valid():
        #     form.save()

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
    print(f"hasil sqlmap : {hasil}")
    form = ScanResultForm({'ScanID': db_id, 'ScanType' : "3", 'Description': hasil})
    form.save()

    global CTR_sqlmap
    CTR_sqlmap=1

def run_script(ip,db_id):
    # run nmap
    run_nmap(ip,db_id, "nmap -sV ")
    # run_nmap(ip,db_id, "nmap -p 1521 ")

    # run sqlmap
    TARGET = Scan.objects.get(pk=db_id)

    # cek kalo packetrequestnya tidak kosong
    if TARGET.PacketRequest != "":
        run_thread_sql(TARGET.PacketRequest,db_id)
    else:
        global CTR_sqlmap
        CTR_sqlmap=1


    # if statement cek kalo status nya fail atau ongoing
    i=0
    while i<=10:
        if CTR_nmap==1 and CTR_sqlmap==1 and CTR_hydra==CTR_hydra_current and CTR==CTR_current:
            if TARGET.Status=="Failed":
                break
            i=11
            UPDATE = Scan.objects.get(pk=db_id)
            UPDATE.Status = "Done"
            UPDATE.save()
        else:
            time.sleep(5)
            