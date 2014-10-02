# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0050_auto_20140921_1940'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='mode',
            field=models.IntegerField(default=0, choices=[(0, b'email'), (1, b'sms')]),
            preserve_default=True,
        ),
    ]
