# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issuer', '0002_auto_20141030_0423'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('address', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('issuer', models.ForeignKey(to='issuer.Issuer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AddressHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField(auto_now_add=True)),
                ('address', models.ForeignKey(to='issuer.Address')),
                ('color', models.ForeignKey(to='issuer.Color')),
                ('issuer', models.ForeignKey(to='issuer.Issuer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ColorHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('color_name', models.CharField(max_length=50)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField(auto_now_add=True)),
                ('address', models.ForeignKey(to='issuer.Address')),
                ('color', models.ForeignKey(to='issuer.Color')),
                ('issuer', models.ForeignKey(to='issuer.Issuer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='historyaddress',
            name='color',
        ),
        migrations.DeleteModel(
            name='HistoryAddress',
        ),
        migrations.RenameField(
            model_name='color',
            old_name='color_number',
            new_name='color_id',
        ),
        migrations.RemoveField(
            model_name='color',
            name='current_address',
        ),
        migrations.DeleteModel(
            name='ActiveAddress',
        ),
        migrations.AddField(
            model_name='color',
            name='address',
            field=models.ForeignKey(default=2, to='issuer.Address'),
            preserve_default=False,
        ),
    ]
