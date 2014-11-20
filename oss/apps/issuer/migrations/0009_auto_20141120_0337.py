# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issuer', '0008_auto_20141120_0306'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalissuer',
            old_name='register_url',
            new_name='url',
        ),
        migrations.RenameField(
            model_name='issuer',
            old_name='register_url',
            new_name='url',
        ),
        migrations.AddField(
            model_name='historicalissuer',
            name='name',
            field=models.CharField(default='a', max_length=20, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='issuer',
            name='name',
            field=models.CharField(default='a', unique=True, max_length=20),
            preserve_default=False,
        ),
    ]
