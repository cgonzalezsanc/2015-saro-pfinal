# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0008_auto_20150520_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='fecha',
            field=models.DateField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuario',
            name='color_fondo',
            field=models.CharField(default=b'd', max_length=1),
            preserve_default=True,
        ),
    ]
