# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0012_auto_20150907_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='add_days_before_event',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='family',
            name='hh_location',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Regent Suite'), (2, b'Shul'), (3, b'Both')]),
            preserve_default=True,
        ),
    ]
