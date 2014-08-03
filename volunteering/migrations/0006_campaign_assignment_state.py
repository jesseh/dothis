# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0005_auto_20140803_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='assignment_state',
            field=models.IntegerField(default=2, verbose_name=b'assignment_state', choices=[(0, b'Assigned'), (1, b'Assignable'), (2, b'Assigned and assignable')]),
            preserve_default=True,
        ),
    ]
