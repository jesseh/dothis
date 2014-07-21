# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0003_auto_20140721_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='obscure_slug',
            field=models.CharField(unique=True, max_length=10, blank=True),
        ),
    ]
