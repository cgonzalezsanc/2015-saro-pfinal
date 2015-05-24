# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0006_auto_20150519_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='duracion',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
    ]
