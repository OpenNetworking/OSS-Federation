# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0002_block'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='block_miner',
            field=models.CharField(max_length=32, db_column=b'block_miner', blank=True),
        ),
    ]
