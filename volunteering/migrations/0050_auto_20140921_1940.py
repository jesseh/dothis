# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.core.exceptions import ObjectDoesNotExist


class Migration(migrations.Migration):

    def rename_content_type_name(apps, schema_editor):
        ContentType = apps.get_model('contenttypes', 'ContentType')
        try:
            c = ContentType.objects.get(model='triggerbydate')
        except ObjectDoesNotExist:
            return
        c.name = 'trigger by date'
        c.save()

    dependencies = [
        ('volunteering', '0049_auto_20140921_1748'),
    ]

    operations = [
        migrations.RunPython(rename_content_type_name),
    ]
