# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0023_auto_20140806_1432'),
    ]

    operations = [
        migrations.CreateModel(
            name='DutyEditable',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name_plural': b'Duties (editable)',
            },
            bases=('volunteering.duty',),
        ),
    ]
