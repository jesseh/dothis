# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0014_auto_20151229_1625'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='is_active',
            new_name='is_visible_to_volunteers',
        ),
    ]
