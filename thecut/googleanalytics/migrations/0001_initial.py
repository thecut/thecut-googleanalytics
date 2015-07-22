# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import oauth2client.django_orm


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('web_property_id', models.CharField(help_text='The property tracking ID is available when viewing the "Tracking Code" details in the Google Analytics admin.', max_length=25, verbose_name='property tracking ID')),
                ('profile_id', models.CharField(default='', max_length=25, verbose_name='view (profile) ID', blank=True)),
                ('display_features', models.BooleanField(default=False, help_text='Used for remarketing, demographics and interest reporting.', verbose_name='Use Display advertising features?')),
                ('is_enabled', models.BooleanField(default=False, help_text='Is Google Analytics tracking enabled on the website?', verbose_name='enabled')),
            ],
            options={
                'ordering': ['site'],
                'verbose_name': 'view (profile)',
                'verbose_name_plural': 'views (profiles)',
            },
        ),
        migrations.CreateModel(
            name='ProfileOAuth2Credentials',
            fields=[
                ('id', models.OneToOneField(related_name='_oauth2_credentials', primary_key=True, serialize=False, to='googleanalytics.Profile')),
                ('credentials', oauth2client.django_orm.CredentialsField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='site',
            field=models.OneToOneField(related_name='+', to='sites.Site'),
        ),
    ]
