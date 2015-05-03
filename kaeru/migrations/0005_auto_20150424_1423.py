# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kaeru', '0004_project_contributors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='page_create_date',
        ),
        migrations.RemoveField(
            model_name='page',
            name='page_modify_date',
        ),
        migrations.RemoveField(
            model_name='page',
            name='user',
        ),
    ]
