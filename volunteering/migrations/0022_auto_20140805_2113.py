# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0021_auto_20140805_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='name',
            field=models.CharField(unique=True, max_length=200),
        ),
    ]
