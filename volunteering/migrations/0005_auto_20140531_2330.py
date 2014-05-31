# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0004_duty_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duty',
            name='tags',
            field=taggit.managers.TaggableManager(to=taggit.models.Tag, through=taggit.models.TaggedItem, blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.DeleteModel(
            name='Label',
        ),
    ]
