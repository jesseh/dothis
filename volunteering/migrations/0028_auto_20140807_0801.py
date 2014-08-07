# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0027_auto_20140806_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='sendable',
            name='sent_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sendable',
            name='send_date',
            field=models.DateField(),
        ),
    ]
