# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
#from edito313.content.models import Content, Options


def default_options(apps, schema_editor):
    Opt = apps.get_model('content', 'Options')
    
    default = Opt(type='', unique='MONTH', uri_prefix='',
                      exclude_from_archive=False)
    default.save()
    page = Opt(type='PAGE', unique='TOTALLY_UNIQUE', uri_prefix='',
                   exclude_from_archive=True)
    page.save()

class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(default_options),
    ]
