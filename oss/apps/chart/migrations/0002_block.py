# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('block_id', models.DecimalField(serialize=False, primary_key=True, decimal_places=0, max_digits=14)),
                ('block_hash', models.CharField(unique=True, max_length=32)),
                ('block_miner', models.CharField(max_length=32, db_column=b'miner', blank=True)),
                ('block_hashmerkleroot', models.CharField(max_length=32, db_column=b'block_hashMerkleRoot', blank=True)),
                ('block_ntime', models.DecimalField(null=True, decimal_places=0, max_digits=20, db_column=b'block_nTime', blank=True)),
                ('block_height', models.DecimalField(null=True, max_digits=14, decimal_places=0, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
