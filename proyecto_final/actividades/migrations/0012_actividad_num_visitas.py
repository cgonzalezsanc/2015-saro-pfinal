# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0011_actualizacioneventos'),
    ]

    operations = [
        migrations.AddField(
            model_name='actividad',
            name='num_visitas',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
