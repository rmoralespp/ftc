# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-15 17:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SGMGU', '0018_auto_20170615_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expediente_aprobado',
            name='fecha_aprobado',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 15, 13, 20, 1, 115000)),
        ),
        migrations.AlterField(
            model_name='ubicacionlaboral',
            name='sexo',
            field=models.CharField(max_length=20),
        ),
    ]
