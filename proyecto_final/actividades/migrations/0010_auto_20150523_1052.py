# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0009_auto_20150523_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='fecha',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
