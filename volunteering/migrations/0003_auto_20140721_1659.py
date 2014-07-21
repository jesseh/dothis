# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0002_duty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duty',
            name='attributes',
            field=models.ManyToManyField(to='volunteering.Attribute', null=True, blank=True),
        ),
    ]
