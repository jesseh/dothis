# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0053_auto_20141219_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='assignment_message_description',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='web_summary_description',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='assignment_message_description',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='web_summary_description',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='assignment_message_description',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='web_summary_description',
            field=models.TextField(default=b'', blank=True),
        ),
    ]
