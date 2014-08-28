# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0037_auto_20140811_1654'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='campaign',
            options={'ordering': (b'name',)},
        ),
        migrations.AlterModelOptions(
            name='sendable',
            options={},
        ),
        migrations.AddField(
            model_name='family',
            name='hh_location_2014',
            field=models.IntegerField(blank=True, null=True, choices=[(0, b'Regent Suite'), (1, b'Shul')]),
            preserve_default=True,
        ),
    ]
