# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0029_message_body_is_html'),
    ]

    operations = [
        migrations.AddField(
            model_name='sendable',
            name='send_failed',
            field=models.BooleanField(default=False, db_index=True),
            preserve_default=True,
        ),
    ]
