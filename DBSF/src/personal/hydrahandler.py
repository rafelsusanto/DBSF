import os
import subprocess
import sys
import time
import threading
from django.conf.urls.static import static
from .models import *
from .forms import *
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#port ambil dari nmap, harus bikin formatting buat output

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