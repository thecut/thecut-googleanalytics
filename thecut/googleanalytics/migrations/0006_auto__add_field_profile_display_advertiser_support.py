# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Profile.display_advertiser_support'
        db.add_column('googleanalytics_profile', 'display_advertiser_support',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Profile.display_advertiser_support'
        db.delete_column('googleanalytics_profile', 'display_advertiser_support')


    models = {
        'googleanalytics.profile': {
            'Meta': {'ordering': "(u'site',)", 'object_name': 'Profile'},
            'display_advertiser_support': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'profile_id': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '25', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'+'", 'unique': 'True', 'to': "orm['sites.Site']"}),
            'web_property_id': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'googleanalytics.profileoauth2credentials': {
            'Meta': {'object_name': 'ProfileOAuth2Credentials'},
            'credentials': ('oauth2client.django_orm.CredentialsField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'_oauth2_credentials'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['googleanalytics.Profile']"})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['googleanalytics']