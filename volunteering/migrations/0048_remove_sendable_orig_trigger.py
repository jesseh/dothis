# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0047_auto_20140921_1301'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sendable',
            name='orig_trigger',
        ),
    ]
