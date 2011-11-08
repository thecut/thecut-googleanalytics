# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_table('googleanalytics_analyticswebproperty',
            'googleanalytics_profile')


    def backwards(self, orm):
        db.rename_table('googleanalytics_profile',
            'googleanalytics_analyticswebproperty')


    models = {
        'googleanalytics.profile': {
            'Meta': {'ordering': "[u'site']", 'object_name': 'Profile'},
            '_oauth2_token': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'+'", 'unique': 'True', 'to': "orm['sites.Site']"}),
            'web_property_id': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['googleanalytics']
