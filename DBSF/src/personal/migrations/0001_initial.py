# Generated by Django 4.1.7 on 2023-04-23 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scans',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('IPAddress', models.CharField(max_length=20)),
                ('PacketRequest', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ScanResults',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ScanType', models.CharField(max_length=3)),
                ('FilePath', models.CharField(max_length=255)),
                ('ScanID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personal.scans')),
            ],
        ),
    ]
