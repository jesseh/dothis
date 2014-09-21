# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.core.exceptions import ObjectDoesNotExist


class Migration(migrations.Migration):

    def rename_content_type(apps, schema_editor):
        ContentType = apps.get_model('contenttypes', 'ContentType')
        try:
            c = ContentType.objects.get(model='trigger')
        except ObjectDoesNotExist:
            return
        c.model = 'triggerbydate'
        c.save()

    dependencies = [
        ('volunteering', '0048_remove_sendable_orig_trigger'),
    ]

    operations = [
        migrations.RunPython(rename_content_type),
        migrations.RenameModel('Trigger', 'TriggerByDate'),
        migrations.RenameField('TriggerByDate', 'fixed_assignment_state',
                               'assignment_state'),
    ]
