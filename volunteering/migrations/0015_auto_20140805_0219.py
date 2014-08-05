# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0014_auto_20140805_0018'),
    ]

    operations = [
        migrations.RenameField(
            model_name='family',
            old_name='family_id',
            new_name='external_id',
        ),
        migrations.RenameField(
            model_name='volunteer',
            old_name='individual_id',
            new_name='external_id',
        ),
        migrations.RenameField(
            model_name='volunteer',
            old_name='family_id',
            new_name='family',
        ),
    ]
