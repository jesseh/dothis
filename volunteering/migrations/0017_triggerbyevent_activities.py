# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0016_auto_20151230_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='triggerbyevent',
            name='activities',
            field=models.ManyToManyField(to='volunteering.Activity', blank=True),
        ),
    ]
