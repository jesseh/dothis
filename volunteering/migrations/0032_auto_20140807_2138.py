# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0031_auto_20140807_2026'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sendable',
            options={},
        ),
        migrations.AlterField(
            model_name='sendable',
            name='send_date',
            field=models.DateField(db_index=True),
        ),
        migrations.AlterField(
            model_name='sendable',
            name='sent_date',
            field=models.DateField(db_index=True, null=True, blank=True),
        ),
    ]
