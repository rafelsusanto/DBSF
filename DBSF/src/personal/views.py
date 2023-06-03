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
        portList = []
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

            # save port number and db type
            if line.find('tcp open  mysql')!=-1 or line.find('tcp  open  mysql')!=-1 or line.find('tcp   open  mysql')!=-1:
                tempDataStore = {}
                tempDataStore["dbType"] = "mysql"
                db_port = line.split('/')
                tempDataStore["portNumber"] = db_port[0]
                portList.append(tempDataStore)
            elif line.find('tcp open  oracle')!=-1 or line.find('tcp  open  oracle')!=-1 or line.find('tcp   open  oracle')!=-1:
                tempDataStore = {}
                tempDataStore["dbType"] = "oracle"
                db_port = line.split('/')
                tempDataStore["portNumber"] = db_port[0]
                portList.append(tempDataStore)
    except:
        pass
    return scan_header , portList

def scanResultAdd(scanResult, dbPort, data,scanType):
    i=0
    for s in scanResult:
        
        if s['portNumber'] == dbPort:
            if scanType == "2":
                scanResult[i]["credential"]=data
            elif scanType == "5":
                scanResult[i]["vulners"]=data
        i+=1
    return scanResult

def scanResultExtract(scan_id, portList):
    scanResult = portList
    scan_list = ScanResult.objects.filter(ScanID=scan_id)
    for sl in scan_list:
        if sl.ScanType == "1":
            pass
        elif sl.ScanType == "2":
            tempData = sl.Description
            tempDataPort = tempData.split('\n')
            tempDataPort = tempDataPort[0]
            scanResult = scanResultAdd(scanResult,tempDataPort, tempData,"2")
        elif sl.ScanType == "5":
            tempData = sl.Description
            tempDataPort = tempData.split('/')
            tempDataPort = tempDataPort[0]
            scanResult = scanResultAdd(scanResult,tempDataPort, tempData,"5")
    return scanResult


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
    scan_header , portList = scanHeader(scan_id)

    # filter result
    scanListResult = scanResultExtract(scan_id, portList)
    # for currPort in portList:
    #     if currPort["dbType"]=="mysql":
    #         tempDataStore["dbType"]="mysql"
    #         tempDataStore["portNumber"]=currPort["portNumber"]

    #         # take vulners data from database
    #         vulnersData = ScanResult.objects.get(ScanID=scan_id,ScanType="5")

    #         credentialData = ScanResult.objects.get(ScanID=scan_id,ScanType="5")
    #     elif currPort["dbType"]=="oracle":
    #         pass
    
        
    return render(request, "scanresult.html",{'failCtr':"Not Failed",'ip':failChecker.IPAddress,'scan_header':scan_header,'scan_list':scanListResult})  