# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0002_auto_20150518_1320'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('color_fondo', models.CharField(default=b'w', max_length=1)),
                ('titulo', models.TextField(default=b'')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='usuarioregistrado',
            name='usuario',
        ),
        migrations.AlterField(
            model_name='actividadelegida',
            name='usuario',
            field=models.ForeignKey(to='actividades.Usuario'),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='UsuarioRegistrado',
        ),
    ]
