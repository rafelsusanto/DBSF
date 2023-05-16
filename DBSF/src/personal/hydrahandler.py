import os
import subprocess
import sys
import threading
from .models import *
from .forms import *

#port ambil dari nmap, harus bikin formatting buat output

def run_thread(ip,port,db_id):
    thread = threading.Thread(target=run_nmap,args=(ip,db_id,))
    thread.setDaemon(True)
    thread.start()

def run_hydra(ip,port,db_id):
    CMD = "hydra -L "+ ip + " " + "3306"
    op = subprocess.run(CMD, shell=True, stdout=subprocess.PIPE)
    hasil = op.stdout
    hasil = hasil.decode('UTF-8')

    #form = ScanResultForm({'ScanID': db_id, 'ScanType' : "1", 'Description': hasil})
    #form.save()

    #UPDATE = Scan.objects.get(pk=db_id)
    #UPDATE.Status = "Done"
    #UPDATE.save()