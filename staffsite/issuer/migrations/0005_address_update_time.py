# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('issuer', '0004_auto_20141103_0611'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='update_time',
            field=models.DateTimeField(default=datetime.date(2014, 11, 3), auto_now=True),
            preserve_default=False,
        ),
    ]
