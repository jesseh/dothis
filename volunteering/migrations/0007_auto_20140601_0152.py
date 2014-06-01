# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0006_auto_20140601_0125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='external_id',
            field=models.CharField(max_length=200, unique=True, null=True, blank=True),
        ),
    ]
