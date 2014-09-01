# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0038_auto_20140828_1334'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='campaign',
            options={'ordering': (b'name',)},
        ),
        migrations.AlterModelOptions(
            name='sendable',
            options={},
        ),
        migrations.AddField(
            model_name='volunteer',
            name='temporary_change',
            field=models.BooleanField(default=False, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='trigger',
            name='event_based_assignment_state',
            field=models.IntegerField(default=2, choices=[(0, b'With an assigned duty'), (1, b'Assignable to a duty'), (2, b'All recipients'), (3, b'No assigned duties')]),
        ),
        migrations.AlterField(
            model_name='trigger',
            name='fixed_assignment_state',
            field=models.IntegerField(default=2, choices=[(0, b'With an assigned duty'), (1, b'Assignable to a duty'), (2, b'All recipients'), (3, b'No assigned duties')]),
        ),
    ]
