# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0035_auto_20140808_2141'),
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
            model_name='volunteer',
            name='note',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
    ]
