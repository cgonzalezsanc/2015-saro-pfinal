# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0007_auto_20150519_1519'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='password',
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nombre',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
