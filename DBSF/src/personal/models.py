from django.db import models

# Create your models here.
class Scan(models.Model):
    Name = models.CharField(max_length=50)
    IPAddress = models.CharField(max_length=20)
    Status = models.CharField(max_length=8, default="On Going")
    PacketRequest = models.FileField(blank=True, null=True, upload_to='pr/')
    Created_at = models.DateTimeField(auto_now_add=True)

class ScanResult(models.Model):
    ScanID = models.ForeignKey(Scan, on_delete=models.CASCADE)
    ScanType = models.CharField(max_length=3)
    Description = models.TextField(null=True)