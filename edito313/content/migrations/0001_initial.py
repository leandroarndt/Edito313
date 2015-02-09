# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers
from django.conf import settings
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('type', models.CharField(choices=[('BLOGPOST', 'blog post'), ('PAGE', 'page'), ('QUOTE', 'quote'), ('IMAGE', 'image'), ('CATEGORY', 'category')], max_length=50)),
                ('title', models.CharField(max_length=200)),
                ('text', ckeditor.fields.RichTextField()),
                ('slug', models.SlugField(max_length=200, blank=True)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('publishing', models.DateTimeField(blank=True)),
                ('editing', models.DateTimeField(auto_now=True)),
                ('published', models.BooleanField(default=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True)),
                ('parent', models.ManyToManyField(null=True, related_name='parent_rel_+', to='content.Content', blank=True)),
                ('tags', taggit.managers.TaggableManager(through='taggit.TaggedItem', verbose_name='Tags', to='taggit.Tag', help_text='A comma-separated list of tags.', blank=True)),
            ],
            options={
                'ordering': ['publishing', 'title'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('type', models.CharField(unique=True, choices=[('BLOGPOST', 'blog post'), ('PAGE', 'page'), ('QUOTE', 'quote'), ('IMAGE', 'image'), ('CATEGORY', 'category')], max_length=50, blank=True)),
                ('unique', models.CharField(default='NONE', choices=[('NONE', 'none'), ('TOTALLY_UNIQUE', 'totally unique'), ('DATE', 'date'), ('MONTH', 'month'), ('YEAR', 'year')], max_length=50)),
                ('uri_prefix', models.CharField(max_length=50, blank=True)),
                ('exclude_from_archive', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'options',
            },
            bases=(models.Model,),
        ),
    ]
