# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields
import taggit.managers
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('type', models.CharField(max_length=50, blank=True, choices=[('BLOGPOST', 'blog post'), ('PAGE', 'page'), ('QUOTE', 'quote'), ('IMAGE', 'image'), ('CATEGORY', 'category')])),
                ('title', models.CharField(max_length=200)),
                ('text', ckeditor.fields.RichTextField()),
                ('slug', models.SlugField(max_length=200, blank=True)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('publishing', models.DateTimeField(blank=True)),
                ('editing', models.DateTimeField(auto_now=True)),
                ('published', models.BooleanField(default=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('parent', models.ManyToManyField(blank=True, null=True, to='content.Content')),
                ('tags', taggit.managers.TaggableManager(verbose_name='Tags', blank=True, through='taggit.TaggedItem', to='taggit.Tag', help_text='A comma-separated list of tags.')),
            ],
            options={
                'ordering': ['publishing', 'title'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('type', models.CharField(max_length=50, unique=True, blank=True, choices=[('BLOGPOST', 'blog post'), ('PAGE', 'page'), ('QUOTE', 'quote'), ('IMAGE', 'image'), ('CATEGORY', 'category'), ('', 'default')])),
                ('unique', models.CharField(max_length=50, default='NONE', choices=[('NONE', 'none'), ('TOTALLY_UNIQUE', 'totally unique'), ('DATE', 'date'), ('MONTH', 'month'), ('YEAR', 'year')])),
                ('uri_prefix', models.CharField(verbose_name='URI prefix', max_length=50, blank=True)),
                ('exclude_from_archive', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'options',
            },
            bases=(models.Model,),
        ),
    ]
