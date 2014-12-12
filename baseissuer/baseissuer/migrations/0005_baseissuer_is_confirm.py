# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('baseissuer', '0004_auto_20141211_0948'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseissuer',
            name='is_confirm',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
