# Generated by Django 4.1.7 on 2023-05-08 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0003_alter_scan_packetrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='scan',
            name='Status',
            field=models.CharField(default='ongoing', max_length=8),
        ),
        migrations.AlterField(
            model_name='scan',
            name='PacketRequest',
            field=models.FileField(blank=True, null=True, upload_to='pr/'),
        ),
    ]
