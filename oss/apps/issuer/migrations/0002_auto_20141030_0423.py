# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('issuer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveAddress',
            fields=[
                ('address', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoryAddress',
            fields=[
                ('address', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField(auto_now_add=True)),
                ('color', models.ForeignKey(to='issuer.Color')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='issuer',
            old_name='date_joined',
            new_name='create_time',
        ),
        migrations.AddField(
            model_name='color',
            name='color_name',
            field=models.CharField(default=datetime.datetime(2014, 10, 30, 4, 22, 22, 49717), unique=True, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='color',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 30, 4, 22, 35, 870216), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='color',
            name='current_address',
            field=models.OneToOneField(default='dsaidja', to='issuer.ActiveAddress'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='color',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 30, 4, 23, 0, 742282), auto_now=True),
            preserve_default=False,
        ),
    ]
