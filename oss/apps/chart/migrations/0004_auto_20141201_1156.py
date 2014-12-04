# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0003_auto_20141201_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='block_hash',
            field=models.CharField(unique=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='block',
            name='block_hashmerkleroot',
            field=models.CharField(max_length=128, db_column=b'block_hashMerkleRoot', blank=True),
        ),
        migrations.AlterField(
            model_name='block',
            name='block_miner',
            field=models.CharField(max_length=128, db_column=b'block_miner', blank=True),
        ),
    ]
