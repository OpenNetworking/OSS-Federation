# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('baseissuer', '0002_auto_20141211_0524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='baseissuer',
            name='is_confirmed',
        ),
    ]
