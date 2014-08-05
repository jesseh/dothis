# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0017_auto_20140805_0316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='activities',
            field=models.ManyToManyField(to=b'volunteering.Activity', null=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='events',
            field=models.ManyToManyField(to=b'volunteering.Event', null=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='locations',
            field=models.ManyToManyField(to=b'volunteering.Location', null=True),
        ),
    ]
