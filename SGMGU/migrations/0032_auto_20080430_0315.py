# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2008-04-30 07:15
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SGMGU', '0031_auto_20170630_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expediente_aprobado',
            name='fecha_aprobado',
            field=models.DateTimeField(default=datetime.datetime(2008, 4, 30, 3, 15, 0, 406000)),
        ),
    ]
