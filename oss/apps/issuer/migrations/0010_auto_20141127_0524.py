# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issuer', '0009_auto_20141120_0337'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalissuer',
            name='account_name',
            field=models.CharField(max_length=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issuer',
            name='account_name',
            field=models.CharField(max_length=20),
            preserve_default=True,
        ),
    ]
