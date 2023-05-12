from django import forms
from .models import *

class ScanForm(forms.ModelForm):
    class Meta:
        model = Scan
        fields = ['Name','IPAddress','PacketRequest']

class ScanResultForm(forms.ModelForm):
    class Meta:
        model = ScanResult
        fields = ['ScanID','ScanType','Description']