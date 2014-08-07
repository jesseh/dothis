# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0026_auto_20140806_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendable',
            name='assignment',
            field=models.ForeignKey(blank=True, to='volunteering.Assignment', null=True),
        ),
    ]
