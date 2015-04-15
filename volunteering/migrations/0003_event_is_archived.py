# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0002_auto_20150410_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_archived',
            field=models.BooleanField(default=False, db_index=True),
            preserve_default=True,
        ),
    ]
