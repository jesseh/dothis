# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0017_triggerbyevent_activities'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duty',
            name='activity',
            field=models.ForeignKey(default=0, to='volunteering.Activity'),
            preserve_default=False,
        ),
    ]
