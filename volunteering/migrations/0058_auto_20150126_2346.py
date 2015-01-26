# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0057_auto_20150126_2232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='is_done',
        ),
        migrations.AddField(
            model_name='event',
            name='is_active',
            field=models.BooleanField(default=True, db_index=True),
            preserve_default=True,
        ),
    ]
