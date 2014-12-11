# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('issuer', '0007_auto_20141103_0928'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalAddress',
            fields=[
                ('address', models.CharField(max_length=50, db_index=True)),
                ('create_time', models.DateTimeField(editable=False, blank=True)),
                ('update_time', models.DateTimeField(editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'verbose_name': 'historical address',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalColor',
            fields=[
                ('color_id', models.BigIntegerField(db_index=True)),
                ('color_name', models.CharField(max_length=50, db_index=True)),
                ('issuer_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('address_id', models.CharField(db_index=True, max_length=50, null=True, blank=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(editable=False, blank=True)),
                ('update_time', models.DateTimeField(editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'verbose_name': 'historical color',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalIssuer',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('user_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('register_url', models.URLField()),
                ('update_time', models.DateTimeField(editable=False, blank=True)),
                ('create_time', models.DateTimeField(editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'verbose_name': 'historical issuer',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='addresshistory',
            name='address',
        ),
        migrations.RemoveField(
            model_name='addresshistory',
            name='color',
        ),
        migrations.RemoveField(
            model_name='addresshistory',
            name='issuer',
        ),
        migrations.DeleteModel(
            name='AddressHistory',
        ),
        migrations.RemoveField(
            model_name='colorhistory',
            name='address',
        ),
        migrations.RemoveField(
            model_name='colorhistory',
            name='color',
        ),
        migrations.RemoveField(
            model_name='colorhistory',
            name='issuer',
        ),
        migrations.DeleteModel(
            name='ColorHistory',
        ),
        migrations.RemoveField(
            model_name='address',
            name='issuer',
        ),
    ]
