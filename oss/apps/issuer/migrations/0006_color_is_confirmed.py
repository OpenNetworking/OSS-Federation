# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issuer', '0005_address_update_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='color',
            name='is_confirmed',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
