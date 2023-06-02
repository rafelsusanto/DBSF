from django.shortcuts import render, redirect
from .forms import *
from .models import *
from .fullscan import *

# create normal function here
def removeWhiteSpace(TeXt):
    ctr = 0
    for x in TeXt:
        if x == ' ':
            ctr+=1
        else:
            break
    return TeXt[ctr:]

def scanHeader(scan_id):
    try:
        scan_header = []
        nmap_result = ScanResult.objects.get(ScanID=scan_id, ScanType= "1")
        nmap_result = nmap_result.Description
        for line in nmap_result.split('\n'):
            data={}
            if line.find('/tcp open ')!=-1:
                tempport = line.split('/tcp open  ')
            elif line.find('/tcp  open ')!=-1:
                tempport = line.split('/tcp  open  ')
            elif line.find('/tcp   open ')!=-1:
                tempport = line.split('/tcp   open  ')
            tempservice = tempport[1].split(' ')
            tempversion = tempport[1].split(str(tempservice[0]))
            data['port']= tempport[0]
            data['service']= tempservice[0]
            data['version']= removeWhiteSpace(tempversion[1])
            scan_header.append(data)
    except:
        pass
    return scan_header

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
    # scan list
    scan_list = ScanResult.objects.filter(ScanID=scan_id)

    # fail checker
    failChecker = Scan.objects.get(pk=scan_id)
    if failChecker.Status=="Failed":
        return render(request, "scanresult.html",{'failCtr':"Failed"})  
    elif failChecker.Status=="On Going":
        return render(request, "scanresult.html",{'failCtr':"On Going"})  
    
    # filter header
    scan_header=scanHeader(scan_id)

    
        
    return render(request, "scanresult.html",{'failCtr':"Not Failed",'ip':failChecker.IPAddress,'scan_header':scan_header,'scan_list':scan_list})  