# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0009_auto_20150809_2105'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='from_address',
            field=models.EmailField(default=b'New North London Security Team <security@nnls-masorti.org.uk>', max_length=75),
            preserve_default=True,
        ),
    ]
