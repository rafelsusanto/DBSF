from django.shortcuts import render, redirect
from .forms import *
from .models import *
from .fullscan import *

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
        
        if form.is_valid():
            form.save()
            l = Scan.objects.all().last()
            # run_nmap(str(l.IPAddress))
            # run script here
            # run(ip)
            run_fullscan(str(l.IPAddress),l.id)

            # redirect to scanlist
            scan_list = Scan.objects.all()
            return render(request, "scanlist.html",{'scan_list':scan_list,'msg' : "Saved"})
    return render(request, "newscan.html")   

def scanlist_screen_view(request, msg="nothing"):
    scan_list = Scan.objects.all()
    return render(request, "scanlist.html",{'scan_list':scan_list,'msg' : msg})   

def delete_scan_list(request, scan_id):
    DELETE = Scan.objects.get(pk=scan_id)
    DELETE.delete()

    return redirect(scanlist_screen_view)

def view_scan_result(request, scan_id):
    # print("test")
    scan_list = ScanResult.objects.filter(ScanID=scan_id)
    # filter output user sini
    failChecker = Scan.objects.get(pk=scan_id)
    if failChecker.Status=="Failed":
        return render(request, "scanresult.html",{'failCtr':"Failed"})  
    return render(request, "scanresult.html",{'failCtr':"Not Failed",'scan_list':scan_list})  