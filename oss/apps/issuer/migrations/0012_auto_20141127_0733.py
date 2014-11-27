# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issuer', '0011_auto_20141127_0721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalissuer',
            name='account_name',
            field=models.CharField(max_length=20, db_index=True),
        ),
        migrations.AlterField(
            model_name='issuer',
            name='account_name',
            field=models.CharField(unique=True, max_length=20),
        ),
    ]
