# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0006_auto_20150809_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triggerbyassignment',
            name='bcc',
            field=models.CharField(help_text=b'comma-seperated email addresses', max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='triggerbydate',
            name='bcc',
            field=models.CharField(help_text=b'comma-seperated email addresses', max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='triggerbyevent',
            name='bcc',
            field=models.CharField(help_text=b'comma-seperated email addresses', max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
