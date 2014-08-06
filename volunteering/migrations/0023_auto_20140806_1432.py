# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0022_auto_20140805_2113'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='activities',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='events',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='locations',
        ),
        migrations.RemoveField(
            model_name='trigger',
            name='campaign',
        ),
        migrations.DeleteModel(
            name='Campaign',
        ),
        migrations.RemoveField(
            model_name='trigger',
            name='message',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.DeleteModel(
            name='Trigger',
        ),
        migrations.AlterModelOptions(
            name='duty',
            options={'verbose_name_plural': b'Duties'},
        ),
    ]
