import os
import subprocess
import sys
import threading
from .models import *
from .forms import *

def run_thread(ip,db_id):
    thread = threading.Thread(target=run_nmap,args=(ip,db_id,))
    thread.setDaemon(True)
    thread.start()

def run_odat(ip,db_id):
    CMD = "odat -h " #ganti ke command apa yg mau di run
    op = subprocess.run(CMD, shell=True, stdout=subprocess.PIPE)
    hasil = op.stdout
    hasil = hasil.decode('UTF-8')

    #form = ScanResultForm({'ScanID': db_id, 'ScanType' : "1", 'Description': hasil})
    #form.save()

    #UPDATE = Scan.objects.get(pk=db_id)
    #UPDATE.Status = "Done"
    #UPDATE.save()
