from django.db import models

# Create your models here.
class Scan(models.Model):
    Name = models.CharField(max_length=50)
    IPAddress = models.CharField(max_length=20)
    PacketRequest = models.FileField(null=True, upload_to='pr/')

class ScanResult(models.Model):
    ScanID = models.ForeignKey(Scan, on_delete=models.CASCADE)
    ScanType = models.CharField(max_length=3)
    FilePath = models.CharField(max_length=255)