# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2008-04-30 05:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SGMGU', '0047_auto_20170804_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expediente_aprobado',
            name='fecha_aprobado',
            field=models.DateTimeField(default=datetime.datetime(2008, 4, 30, 1, 27, 23, 718000)),
        ),
    ]
