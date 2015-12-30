# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0015_auto_20151230_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='is_visible_to_volunteers',
            field=models.BooleanField(default=True, db_index=True),
        ),
    ]
