# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0016_auto_20140805_0305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='email_address',
            field=models.EmailField(max_length=75, blank=True),
        ),
    ]
