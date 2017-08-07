# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-02 19:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SGMGU', '0038_auto_20170802_1455'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inhabilitacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_resolucion', models.IntegerField()),
                ('fecha_inhabilitacion', models.DateTimeField(auto_now_add=True)),
                ('graduado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGMGU.GraduadoInhabilitacion')),
            ],
        ),
        migrations.CreateModel(
            name='Suspension',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_resolucion', models.IntegerField()),
                ('fecha_suspension', models.DateTimeField(auto_now_add=True)),
                ('graduado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGMGU.GraduadoInhabilitacion')),
            ],
        ),
        migrations.AlterField(
            model_name='expediente_aprobado',
            name='fecha_aprobado',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 2, 15, 55, 10, 431000)),
        ),
    ]
