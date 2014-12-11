# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tx',
            fields=[
                ('tx_id', models.DecimalField(serialize=False, primary_key=True, decimal_places=0, max_digits=26)),
                ('tx_hash', models.CharField(max_length=255)),
                ('tx_type', models.IntegerField(null=True, blank=True)),
                ('tx_color', models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)),
                ('total_in', models.DecimalField(max_digits=30, decimal_places=0)),
                ('total_out', models.DecimalField(max_digits=30, decimal_places=0)),
                ('tx_ntime', models.DecimalField(null=True, decimal_places=0, max_digits=20, db_column=b'tx_nTime', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
