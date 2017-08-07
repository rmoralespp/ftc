# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-02 20:12
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SGMGU', '0040_auto_20170802_1606'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='graduadoinhabilitacion',
            name='causal_incumplimiento',
        ),
        migrations.AddField(
            model_name='inhabilitacion',
            name='causal_incumplimiento',
            field=models.CharField(choices=[(b'sp', b'Salida del pa\xc3\xads'), (b'd', b'Desmotivaci\xc3\xb3n'), (b'pp', b'Problemas Personales'), (b'eol', b'Ejerce otra labor'), (b'o', b'Otras')], default=1, max_length=90),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='suspension',
            name='causal_incumplimiento',
            field=models.CharField(choices=[(b'h', b'Habilitaci\xc3\xb3n'), (b'o', b'Otras')], default='1', max_length=90),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='expediente_aprobado',
            name='fecha_aprobado',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 2, 16, 12, 6, 832000)),
        ),
    ]