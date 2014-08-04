# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0010_auto_20140803_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='duty',
            name='details',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
