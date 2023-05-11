import os
import subprocess
import sqlmap
import sys
import threading
from .models import *
from .forms import *

def run_thread(ip,db_id):
    thread = threading.Thread(target=run_nmap,args=(ip,db_id,))
    thread.setDaemon(True)
    thread.start()

def run_nmap(ip,db_id):
    CMD = "nmap -p 80 "+ ip
    op = subprocess.run(CMD, shell=True, stdout=subprocess.PIPE)
    hasil = op.stdout
    hasil = hasil.decode('UTF-8')

    form = ScanResultForm({'ScanID': db_id, 'ScanType' : "1", 'Description': hasil})
    form.save()

    UPDATE = Scan.objects.get(pk=db_id)
    UPDATE.Status = "Done"
    UPDATE.save()



    print(hasil)

def test_ls():
    cmd = "ls"
    op = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    print(op.stdout)
