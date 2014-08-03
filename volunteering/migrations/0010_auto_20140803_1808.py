# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0009_auto_20140803_1757'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trigger',
            old_name='when_relative',
            new_name='days_after_assignment',
        ),
        migrations.AddField(
            model_name='trigger',
            name='days_before_event',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.RenameField(
            model_name='trigger',
            old_name='when_fixed',
            new_name='fixed_date',
        ),
    ]
