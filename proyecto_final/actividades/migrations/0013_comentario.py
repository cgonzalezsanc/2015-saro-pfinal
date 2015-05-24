# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0012_actividad_num_visitas'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField()),
                ('contenido', models.TextField()),
                ('actividad', models.ForeignKey(to='actividades.Actividad')),
                ('usuario', models.ForeignKey(to='actividades.Usuario')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
