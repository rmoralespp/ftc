# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-02 18:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SGMGU', '0010_auto_20170317_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='organismo',
            name='hijode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SGMGU.Organismo'),
        ),
        migrations.AlterField(
            model_name='expediente_aprobado',
            name='fecha_aprobado',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 2, 14, 35, 49, 426000)),
        ),
    ]
