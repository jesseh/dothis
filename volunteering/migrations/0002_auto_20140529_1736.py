# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='duty',
            name='assigned_to',
            field=models.ForeignKey(to_field='id', blank=True, to='volunteering.Volunteer', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='duty',
            name='campaign',
            field=models.ForeignKey(to='volunteering.Campaign', to_field='id'),
        ),
    ]
