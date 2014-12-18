# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('baseissuer', '0005_baseissuer_is_confirm'),
    ]

    operations = [
        migrations.RenameField(
            model_name='baseissuer',
            old_name='is_confirm',
            new_name='is_confirmed',
        ),
    ]
