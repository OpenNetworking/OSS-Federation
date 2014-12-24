# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('baseissuer', '0006_auto_20141218_0905'),
    ]

    operations = [
        migrations.AddField(
            model_name='color',
            name='is_confirming',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
