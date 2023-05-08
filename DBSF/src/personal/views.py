from django.shortcuts import render, redirect
from .forms import ScanForm
from .models import *
from .odathandler import *
from .nmaphandler import *
from .sqlhandler import *

# Create your views here.
def home_screen_view(request):
    # print(request.headers)
    return render(request, "home.html",{})

def result_screen_view(request):
    # print(request.headers)
    
    return render(request, "result.html",{})

def newscan(request):
    # print(request.headers)
    if request.method == "POST":
        form = ScanForm(request.POST, request.FILES)
        print(form)
        print(request.FILES)
        # test_ls()
        if form.is_valid():
            form.save()
            l = Scan.objects.all().last()
            run_nmap(str(l.IPAddress))

            # redirect to scanlist
            scan_list = Scan.objects.all()
            return render(request, "scanlist.html",{'scan_list':scan_list,'msg' : "Saved"})
    return render(request, "newscan.html")   

def scanlist_screen_view(request, msg="nothing"):
    scan_list = Scan.objects.all()
    return render(request, "scanlist.html",{'scan_list':scan_list,'msg' : msg})   

def delete_scan_list(request, scan_id):
    print(scan_id)
    DELETE = Scan.objects.get(pk=scan_id)
    DELETE.delete()

    return redirect(scanlist_screen_view)