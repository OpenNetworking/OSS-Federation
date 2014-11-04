# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issuer', '0006_color_is_confirmed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='is_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
