# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0005_auto_20150519_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='precio',
            field=models.IntegerField(),
            preserve_default=True,
        ),
    ]
