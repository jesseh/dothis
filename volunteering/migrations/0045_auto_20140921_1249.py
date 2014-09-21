# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0044_auto_20140921_0908'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sendable',
            old_name='trigger',
            new_name='orig_trigger',
        ),
        migrations.AlterUniqueTogether(
            name='sendable',
            unique_together=set([('send_date', 'orig_trigger', 'volunteer', 'assignment')]),
        ),
    ]
