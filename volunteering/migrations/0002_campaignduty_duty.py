# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaignduty',
            name='duty',
            field=models.ForeignKey(to='volunteering.Duty', to_field='id'),
            preserve_default=True,
        ),
    ]
