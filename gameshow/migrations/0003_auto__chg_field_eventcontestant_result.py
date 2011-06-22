# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'EventContestant.result'
        db.alter_column('gameshow_eventcontestant', 'result', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))


    def backwards(self, orm):
        
        # Changing field 'EventContestant.result'
        db.alter_column('gameshow_eventcontestant', 'result', self.gf('django.db.models.fields.CharField')(default='', max_length=100))


    models = {
        'gameshow.contestant': {
            'Meta': {'object_name': 'Contestant'},
            'gameshow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contestants'", 'to': "orm['gameshow.Gameshow']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'gameshow.event': {
            'Meta': {'object_name': 'Event'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'gameshow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'to': "orm['gameshow.Gameshow']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'gameshow.eventcontestant': {
            'Meta': {'object_name': 'EventContestant'},
            'contestant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contestant'", 'to': "orm['gameshow.Contestant']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'to': "orm['gameshow.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'gameshow.gameshow': {
            'Meta': {'object_name': 'Gameshow'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'season': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['gameshow']
