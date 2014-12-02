# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def update_account_name(apps, schema_editor):
    Issuer = apps.get_model('issuer', 'Issuer')
    for issuer in Issuer.objects.all():
        issuer.account_name = issuer.name
        for issuer_history in issuer.history.all():
            issuer_history.account_name = issuer.name
        issuer.save()


class Migration(migrations.Migration):

    dependencies = [
        ('issuer', '0010_auto_20141127_0524'),
    ]

    operations = [
        migrations.RunPython(update_account_name),
    ]
