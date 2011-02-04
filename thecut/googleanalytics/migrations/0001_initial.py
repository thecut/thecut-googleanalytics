# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'AnalyticsWebProperty'
        db.create_table('googleanalytics_analyticswebproperty', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sites.Site'], unique=True)),
            ('web_property_id', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('is_enabled', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
        ))
        db.send_create_signal('googleanalytics', ['AnalyticsWebProperty'])


    def backwards(self, orm):
        
        # Deleting model 'AnalyticsWebProperty'
        db.delete_table('googleanalytics_analyticswebproperty')


    models = {
        'googleanalytics.analyticswebproperty': {
            'Meta': {'object_name': 'AnalyticsWebProperty'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sites.Site']", 'unique': 'True'}),
            'web_property_id': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'sites.site': {
            'Meta': {'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['googleanalytics']
