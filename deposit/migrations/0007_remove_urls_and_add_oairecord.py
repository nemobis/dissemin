# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-26 13:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion

def find_oairecords(apps, schema_editor):
    DepositRecord = apps.get_model('deposit','DepositRecord')
    OaiRecord = apps.get_model('papers', 'OaiRecord')
    for d in DepositRecord.objects.all():
        try:
            r = OaiRecord.objects.get(identifier='deposition:%d:%s'
                % (d.repository_id, d.identifier))
            d.oairecord = r
            d.save()
        except OaiRecord.DoesNotExist:
            pass

def backwards(*args):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('papers', '0039_populate_oai_sources'),
        ('deposit', '0006_depositrecord_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='depositrecord',
            name='pdf_url',
        ),
        migrations.RemoveField(
            model_name='depositrecord',
            name='splash_url',
        ),
        migrations.AddField(
            model_name='depositrecord',
            name='oairecord',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='papers.OaiRecord'),
        ),
        migrations.AlterField(
            model_name='depositrecord',
            name='status',
            field=models.CharField(choices=[('failed', 'Failed'), ('faked', 'Faked'), ('pending', 'Pending publication'), ('published', 'Published'), ('refused', 'Refused by the repository'), ('deleted', 'Deleted')], max_length=64),
        ),
        migrations.RunPython(find_oairecords, backwards),
    ]
