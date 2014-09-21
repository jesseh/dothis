# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('volunteering', '0045_auto_20140921_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='sendable',
            name='trigger_id',
            field=models.PositiveIntegerField(default=999),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sendable',
            name='trigger_type',
            field=models.ForeignKey(default=1, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='sendable',
            unique_together=set([('send_date', 'trigger_type', 'trigger_id', 'volunteer', 'assignment')]),
        ),
    ]
