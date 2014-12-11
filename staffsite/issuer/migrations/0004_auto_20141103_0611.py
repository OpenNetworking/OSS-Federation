# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issuer', '0003_auto_20141103_0606'),
    ]

    operations = [
        migrations.RenameField(
            model_name='color',
            old_name='create_date',
            new_name='create_time',
        ),
        migrations.RenameField(
            model_name='color',
            old_name='update_date',
            new_name='update_time',
        ),
    ]
