# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0011_auto_20150809_2236'),
    ]

    operations = [
        migrations.RenameField(
            model_name='family',
            old_name='hh_location_2014',
            new_name='hh_location',
        ),
    ]
