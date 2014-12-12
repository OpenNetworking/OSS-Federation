# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('baseissuer', '0003_remove_baseissuer_is_confirmed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='baseissuer',
            options={'verbose_name': 'issuer'},
        ),
    ]
