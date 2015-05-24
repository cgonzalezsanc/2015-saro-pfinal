# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0004_auto_20150518_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='duracion',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
