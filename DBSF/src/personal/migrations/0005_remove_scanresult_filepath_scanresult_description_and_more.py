# Generated by Django 4.1.7 on 2023-05-11 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0004_scan_status_alter_scan_packetrequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scanresult',
            name='FilePath',
        ),
        migrations.AddField(
            model_name='scanresult',
            name='Description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='scan',
            name='Status',
            field=models.CharField(default='On Going', max_length=8),
        ),
    ]
