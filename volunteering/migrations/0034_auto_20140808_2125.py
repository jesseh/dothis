# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0033_auto_20140807_2140'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attribute',
            options={'ordering': (b'name',)},
        ),
        migrations.AlterModelOptions(
            name='campaign',
            options={'ordering': (b'name',)},
        ),
        migrations.AlterModelOptions(
            name='duty',
            options={'ordering': [b'event', b'start_time', b'activity', b'location'], 'verbose_name_plural': b'Duties'},
        ),
        migrations.AlterModelOptions(
            name='family',
            options={'ordering': [b'external_id']},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': [b'name']},
        ),
        migrations.AlterModelOptions(
            name='sendable',
            options={},
        ),
        migrations.AlterModelOptions(
            name='trigger',
            options={'ordering': [b'campaign']},
        ),
        migrations.AlterModelOptions(
            name='volunteer',
            options={'ordering': [b'surname']},
        ),
        migrations.AddField(
            model_name='volunteer',
            name='last_summary_view',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
