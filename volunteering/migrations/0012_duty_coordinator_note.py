# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0011_duty_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='duty',
            name='coordinator_note',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
