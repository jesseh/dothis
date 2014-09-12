# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0039_auto_20140901_2002'),
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
            model_name='assignment',
            name='specific_location',
            field=models.ForeignKey(blank=True, to='volunteering.Location', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='family',
            name='hh_location_2014',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Regent Suite'), (2, b'Shul')]),
        ),
    ]
