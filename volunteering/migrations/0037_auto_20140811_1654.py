# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0036_auto_20140810_1255'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='campaign',
            options={'ordering': (b'name',)},
        ),
        migrations.AlterModelOptions(
            name='sendable',
            options={},
        ),
    ]
