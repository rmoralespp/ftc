# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-16 15:29
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SGMGU', '0002_auto_20170216_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expediente',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 16, 10, 29, 59, 154000)),
        ),
        migrations.AlterField(
            model_name='expediente',
            name='graduado',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SGMGU.Graduado'),
        ),
        migrations.AlterField(
            model_name='expediente_aprobado',
            name='fecha_aprobado',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 16, 10, 29, 59, 159000)),
        ),
        migrations.AlterField(
            model_name='expediente_no_aprobado',
            name='fecha_no_aprobado',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 16, 10, 29, 59, 160000)),
        ),
        migrations.AlterField(
            model_name='expediente_pendiente',
            name='fecha_pendiente',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 16, 10, 29, 59, 158000)),
        ),
        migrations.AlterField(
            model_name='expediente_rechazado',
            name='fecha_rechazo',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 16, 10, 29, 59, 158000)),
        ),
        migrations.AlterField(
            model_name='perfil_usuario',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
