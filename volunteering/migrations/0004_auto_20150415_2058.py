# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0003_event_is_archived'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='is_active',
            field=models.BooleanField(default=True, help_text=b'Not available to volunteers.', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='is_archived',
            field=models.BooleanField(default=False, help_text=b'Exclude from future campaigns.', db_index=True),
            preserve_default=True,
        ),
    ]
