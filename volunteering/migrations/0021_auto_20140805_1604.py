# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0020_auto_20140805_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='first_name',
            field=models.CharField(db_index=True, max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='surname',
            field=models.CharField(max_length=200, db_index=True),
        ),
    ]
