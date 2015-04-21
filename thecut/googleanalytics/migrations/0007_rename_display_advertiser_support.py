# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_column('googleanalytics_profile',
                         'display_advertiser_support',
                         'display_features')

    def backwards(self, orm):
        db.rename_column('googleanalytics_profile',
                         'display_features',
                         'display_advertiser_support')

    models = {
        u'googleanalytics.profile': {
            'Meta': {'ordering': "(u'site',)", 'object_name': 'Profile'},
            'display_advertiser_support': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'profile_id': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '25', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'+'", 'unique': 'True', 'to': u"orm['sites.Site']"}),
            'web_property_id': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        u'googleanalytics.profileoauth2credentials': {
            'Meta': {'object_name': 'ProfileOAuth2Credentials'},
            'credentials': ('oauth2client.django_orm.CredentialsField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'_oauth2_credentials'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['googleanalytics.Profile']"})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['googleanalytics']
