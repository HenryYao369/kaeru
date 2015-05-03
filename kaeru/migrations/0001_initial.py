# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filePathAndName', models.CharField(max_length=124)),
                ('created', models.DateTimeField(verbose_name=b'creation date')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=200)),
                ('page_create_date', models.DateTimeField(verbose_name=b'Date created')),
                ('page_modify_date', models.DateTimeField(verbose_name=b'Date modified')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('hidden', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(verbose_name=b'date created')),
                ('creator', models.ForeignKey(related_name='project_creator', default=None, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='page',
            name='project',
            field=models.ForeignKey(to='kaeru.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='page',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='code',
            name='page',
            field=models.ForeignKey(to='kaeru.Page'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='code',
            name='projects',
            field=models.ManyToManyField(related_name='codes', to='kaeru.Project'),
            preserve_default=True,
        ),
    ]
