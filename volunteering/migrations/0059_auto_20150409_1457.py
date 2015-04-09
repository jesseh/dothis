# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0058_auto_20150126_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='dear_name',
            field=models.CharField(help_text=b'Leave blank if same as first name', max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='external_id',
            field=models.CharField(default=0, unique=True, max_length=200),
            preserve_default=False,
        ),
    ]
