# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0019_auto_20140805_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='duty',
            name='coordinator_note',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='duty',
            name='details',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='body',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='home_phone',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='mobile_phone',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
