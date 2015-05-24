# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('titulo', models.TextField()),
                ('gratuito', models.IntegerField()),
                ('precio', models.IntegerField(default=0)),
                ('fecha', models.DateTimeField()),
                ('duracion', models.TimeField()),
                ('larga_duracion', models.IntegerField()),
                ('url_inf_adicional', models.URLField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ActividadElegida',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('fecha_eleccion', models.DateTimeField()),
                ('actividad', models.ForeignKey(to='actividades.Actividad')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('color_fondo', models.CharField(default=b'w', max_length=1)),
                ('titulo', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='actividadelegida',
            name='usuario',
            field=models.ForeignKey(to='actividades.Usuario'),
            preserve_default=True,
        ),
    ]
