# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0003_auto_20150518_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='titulo',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
    ]
