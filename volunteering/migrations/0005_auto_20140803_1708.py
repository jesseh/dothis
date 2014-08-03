# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0004_auto_20140803_1701'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'ordering': [b'name']},
        ),
        migrations.AlterModelOptions(
            name='campaign',
            options={'ordering': (b'-modified', b'-created'), 'get_latest_by': b'modified'},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': [b'date']},
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': [b'name']},
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='activate_date',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='deactivate_date',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='status',
        ),
    ]
