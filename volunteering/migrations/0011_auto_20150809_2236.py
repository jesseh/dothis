# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0010_campaign_from_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='from_address',
            field=models.CharField(default=b'New North London Security Team <security@nnls-masorti.org.uk>', max_length=255),
            preserve_default=True,
        ),
    ]
