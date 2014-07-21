# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0004_auto_20140721_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='external_id',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
