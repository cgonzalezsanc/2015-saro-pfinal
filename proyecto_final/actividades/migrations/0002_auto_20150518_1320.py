# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('actividades', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsuarioRegistrado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('color_fondo', models.CharField(default=b'w', max_length=1)),
                ('titulo', models.TextField(default=b'Pagina de ')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='actividad',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='actividadelegida',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='actividadelegida',
            name='usuario',
            field=models.ForeignKey(to='actividades.UsuarioRegistrado'),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='Usuario',
        ),
    ]
