from django.shortcuts import render, redirect
from .forms import *
from .models import *
from .fullscan import *
from django.core.paginator import Paginator
from django import template
from django.utils.safestring import mark_safe
from django.contrib import messages

register = template.Library()

@register.filter()
def nbsp(value):
    return mark_safe("&nbsp;".join(value.split(' ')))

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
        # print(nmap_result)
        for line in nmap_result.split('\n'):
            data={}
            data['state']="open"
            data['tns'] = "Empty"
            data['vulners'] = "Empty"
            data['sid'] = "Empty"
            data['credential'] = []
            if line.find('/tcp open     ')!=-1:
                tempport = line.split('/tcp open     ')
            elif line.find('/tcp  open     ')!=-1:
                tempport = line.split('/tcp  open     ')
            elif line.find('/tcp   open     ')!=-1:
                tempport = line.split('/tcp   open     ')
            elif line.find('/tcp open ')!=-1:
                tempport = line.split('/tcp open  ')
            elif line.find('/tcp  open ')!=-1:
                tempport = line.split('/tcp  open  ')
            elif line.find('/tcp   open ')!=-1:
                tempport = line.split('/tcp   open  ')
            elif line.find('/tcp filtered ')!=-1  :
                data['state']="filtered"
                tempport = line.split('/tcp filtered ')
            elif line.find('/tcp  filtered ')!=-1:
                data['state']="filtered"
                tempport = line.split('/tcp  filtered ')
            elif line.find('/tcp   filtered ')!=-1:
                data['state']="filtered"
                tempport = line.split('/tcp   filtered ')
            tempservice = tempport[1].split(' ')
            tempversion = tempport[1].split(str(tempservice[0]))
            data['port']= tempport[0]
            data['service']= tempservice[0]
            data['version']= removeWhiteSpace(tempversion[1])
            scan_header.append(data)

            # save port number and db type
            if line.find('tcp open  mysql')!=-1 or line.find('tcp  open  mysql')!=-1 or line.find('tcp   open  mysql')!=-1 or line.find('tcp open     mysql')!=-1 or line.find('tcp  open     mysql')!=-1 or line.find('tcp   open     mysql')!=-1:
                tempDataStore = {}
                tempDataStore["dbType"] = "mysql"
                db_port = line.split('/')
                tempDataStore["portNumber"] = db_port[0]
                portList.append(tempDataStore)
            elif line.find('tcp open  oracle')!=-1 or line.find('tcp  open  oracle')!=-1 or line.find('tcp   open  oracle')!=-1 or line.find('tcp open     oracle')!=-1 or line.find('tcp  open     oracle')!=-1 or line.find('tcp   open     oracle')!=-1:
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
                credList = []
                for d in data.split('\n'):
                    tempDic = {}
                    d = d.split("###")
                    tempDic["username"]=d[0]
                    tempDic["password"]=d[1]
                    credList.append(tempDic)
                scanResult[i]["credential"]=credList 
                
            elif scanType == "4":
                scanResult[i]["sid"]=data
            elif scanType == "5":
                scanResult[i]["vulners"]=data
            elif scanType == "6":
                scanResult[i]["tns"]=data
        i+=1

    return scanResult

def scanResultExtract(scan_id, portList):
    scanResult = portList
    scan_list = ScanResult.objects.filter(ScanID=scan_id)
    sqlResult = ""
    for sl in scan_list:
        if sl.ScanType == "1":
            pass
        elif sl.ScanType == "2":
            tempData = sl.Description
            tempDataPort = tempData.split('\n')
            tempDataPort = tempDataPort[0]
            # ngambil sid list
            index =0 
            for tempLine in tempData:
                index+=1
                if tempLine == '\n':
                    break
            scanResult = scanResultAdd(scanResult,str(tempDataPort), tempData[index:],"2")
        elif sl.ScanType == "3":
            tempData = sl.Description
            tempData = tempData.split('[*] starting')
            sqlResult = nbsp("[*] starting"+tempData[1])
        elif sl.ScanType == "4":
            tempData = sl.Description
            tempDataPort = tempData.split('\n')
            tempDataPort = tempDataPort[0]

            # ngambil sid list
            index =0 
            for tempLine in tempData:
                index+=1
                if tempLine == '\n':
                    break
            scanResult = scanResultAdd(scanResult,tempDataPort, tempData[index:],"4")
        elif sl.ScanType == "5":
            tempData = sl.Description
            tempDataPort = tempData.split('/')
            tempDataPort = tempDataPort[0]
            # proccesss
            tempData = nbsp(tempData)
            scanResult = scanResultAdd(scanResult,tempDataPort, tempData,"5")
        elif sl.ScanType == "6":
            tempData = sl.Description
            tempDataPort = tempData.split('\n')
            tempDataPort = tempDataPort[0]
            if tempData.find("The target is not vulnerable to a remote TNS poisoning"):
                scanResult = scanResultAdd(scanResult,tempDataPort, "Not Vulnerable","6")
            else:
                tempData = "Vulnerable ->  " + nbsp(tempData)
                scanResult = scanResultAdd(scanResult,tempDataPort, tempData,"6")
    return scanResult, sqlResult


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

            messages.success(request, 'success')

            return redirect(scanlist_screen_view)
    return render(request, "newscan.html")   

def scanlist_screen_view(request, msg="nothing"):
    scan_list = Scan.objects.all()
    paginator = Paginator(scan_list, 8)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'msg' : msg
    }

    return render(request, "scanlist.html", context)   

def delete_scan_list(request, scan_id):
    DELETE = Scan.objects.get(pk=scan_id)
    DELETE.delete()

    messages.error(request, 'delete')

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
    sqlResult = ""
    scanListResult, sqlResult = scanResultExtract(scan_id, portList)
    
    # print(f"sqlResult = {sqlResult}")
        
    return render(request, "scanresult.html",{'failCtr':"Not Failed",'ip':failChecker.IPAddress,'scan_header':scan_header,'scan_list':scanListResult, 'sql_result':sqlResult})  