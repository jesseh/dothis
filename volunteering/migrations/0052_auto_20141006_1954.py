# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0051_message_mode'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='triggerbydate',
            options={},
        ),
        migrations.AlterModelOptions(
            name='triggerbyevent',
            options={},
        ),
        migrations.RenameField(
            model_name='activity',
            old_name='description',
            new_name='web_summary_description',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='description',
            new_name='web_summary_description',
        ),
        migrations.RenameField(
            model_name='location',
            old_name='description',
            new_name='web_summary_description',
        ),
        migrations.AddField(
            model_name='activity',
            name='assignment_message_description',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='assignment_message_description',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='assignment_message_description',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='body_is_html',
            field=models.BooleanField(default=False, help_text=b'not used for SMS'),
        ),
        migrations.AlterField(
            model_name='message',
            name='subject',
            field=models.CharField(help_text=b'not used for SMS', max_length=200),
        ),
        migrations.AlterField(
            model_name='triggerbyevent',
            name='assignment_state',
            field=models.IntegerField(default=0, choices=[(0, b'With an assigned duty')]),
        ),
    ]
