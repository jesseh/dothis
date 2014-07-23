# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0005_auto_20140721_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='slug',
            field=models.SlugField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='duty',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
    ]
