import os
import subprocess
import sys
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
    STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]
    password_path = STATICFILES_DIRS[0] + "/files/password.txt"
    print(password_path)

    # hydra -l dvwa -P ./password 127.0.0.1 mysql
    CMD = "hydra -l dvwa -P "+password_path+" " + ip + " " + db_type + " -s " + db_port
    op = subprocess.run(CMD, shell=True, stdout=subprocess.PIPE)
    hasil = op.stdout
    hasil = hasil.decode('UTF-8')
    
    form = ScanResultForm({'ScanID': db_id, 'ScanType' : "2", 'Description': hasil})
    form.save()


    
    print(STATICFILES_DIRS)

    #form = ScanResultForm({'ScanID': db_id, 'ScanType' : "1", 'Description': hasil})
    #form.save()

    #UPDATE = Scan.objects.get(pk=db_id)
    #UPDATE.Status = "Done"
    #UPDATE.save()