# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-15 17:19
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SGMGU', '0017_auto_20170615_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expediente_aprobado',
            name='fecha_aprobado',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 15, 13, 19, 3, 264000)),
        ),
        migrations.AlterField(
            model_name='ubicacionlaboral',
            name='sexo',
            field=models.CharField(choices=[((b'masculino', b'Masculino'), (b'femenino', b'Femenino'))], max_length=20),
        ),
    ]
