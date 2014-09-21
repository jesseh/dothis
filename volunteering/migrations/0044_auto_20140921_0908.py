# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0043_auto_20140921_0907'),
    ]

    operations = [
        migrations.RenameField(
            model_name='triggerbyevent',
            old_name='days_before_event',
            new_name='days_before',
        ),
    ]
