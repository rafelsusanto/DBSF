from django.shortcuts import render

# Create your views here.
def home_screen_view(request):
    # print(request.headers)
    return render(request, "home.html",{})

def result_screen_view(request):
    # print(request.headers)
    return render(request, "result.html",{})

def newscan_screen_view(request):
    # print(request.headers)
    return render(request, "newscan.html",{})   

def scanlist_screen_view(request):
    # print(request.headers)
    return render(request, "scanlist.html",{})   