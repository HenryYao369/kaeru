# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kaeru', '0005_auto_20150424_1423'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='code',
            name='created',
        ),
        migrations.RemoveField(
            model_name='code',
            name='filePathAndName',
        ),
        migrations.RemoveField(
            model_name='code',
            name='projects',
        ),
        migrations.AddField(
            model_name='code',
            name='code',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
    ]
