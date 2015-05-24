# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0010_auto_20150523_1052'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActualizacionEventos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField()),
                ('usuario', models.ForeignKey(to='actividades.Usuario')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
