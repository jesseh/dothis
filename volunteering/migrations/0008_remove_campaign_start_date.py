# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0007_campaign_start_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='start_date',
        ),
    ]
