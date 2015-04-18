# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0004_auto_20150415_2058'),
    ]

    operations = [
        migrations.CreateModel(
            name='VolunteerAdded',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name_plural': 'Recently added volunteers',
            },
            bases=('volunteering.volunteer',),
        ),
    ]
