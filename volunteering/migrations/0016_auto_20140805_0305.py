# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0015_auto_20140805_0219'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteer',
            name='slug',
            field=models.CharField(default='', unique=True, max_length=10, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='family',
            field=models.ForeignKey(to='volunteering.Family'),
        ),
    ]
