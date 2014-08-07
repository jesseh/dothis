# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0028_auto_20140807_0801'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='body_is_html',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
