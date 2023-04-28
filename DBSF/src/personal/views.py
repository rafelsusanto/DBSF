from django.shortcuts import render
from .forms import ScanForm
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
        # print(form)
        if form.is_valid():
            form.save()
        
    return render(request, "newscan.html",{})   

def scanlist_screen_view(request):
    # print(request.headers)
    return render(request, "scanlist.html",{})   