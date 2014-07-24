# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0006_auto_20140723_1735'),
    ]

    operations = [
        migrations.RenameField(
            model_name='volunteer',
            old_name='obscure_slug',
            new_name='slug',
        ),
    ]
