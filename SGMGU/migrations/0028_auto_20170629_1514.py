# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-29 19:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SGMGU', '0027_auto_20170629_1254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='disponibilidadgraduados',
            name='anno_graduado',
        ),
        migrations.AlterField(
            model_name='expediente_aprobado',
            name='fecha_aprobado',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 29, 15, 14, 34, 95000)),
        ),
    ]
