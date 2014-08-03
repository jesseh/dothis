# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0002_auto_20140731_1749'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='short_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='short_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='location',
            old_name='short_description',
            new_name='description',
        ),
    ]
