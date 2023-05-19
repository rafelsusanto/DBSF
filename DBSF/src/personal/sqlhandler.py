import os
import subprocess
import sys
import threading
from .models import *
from .forms import *
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


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
