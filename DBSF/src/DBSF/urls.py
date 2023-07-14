"""DBSF URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from personal.views import(
    home_screen_view,
    result_screen_view,
    newscan,
    scanlist_screen_view,
    delete_scan_list,
    view_scan_result,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_screen_view),
    path('result', result_screen_view),
    path('newscan', newscan),
    path('scanlist', scanlist_screen_view, name="scanlist"),
    path('delete_scan_list/<scan_id>', delete_scan_list),
    path('view_scan_result/<scan_id>', view_scan_result)
]
