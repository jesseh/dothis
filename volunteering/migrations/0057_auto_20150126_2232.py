# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0056_event_is_past'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='is_past',
            new_name='is_done',
        ),
    ]
