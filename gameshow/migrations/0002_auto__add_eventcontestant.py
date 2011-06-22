# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'EventContestant'
        db.create_table('gameshow_eventcontestant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='events', to=orm['gameshow.Event'])),
            ('contestant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='contestant', to=orm['gameshow.Contestant'])),
            ('place', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('result', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('gameshow', ['EventContestant'])

        # Removing M2M table for field contestants on 'Event'
        db.delete_table('gameshow_event_contestants')


    def backwards(self, orm):
        
        # Deleting model 'EventContestant'
        db.delete_table('gameshow_eventcontestant')

        # Adding M2M table for field contestants on 'Event'
        db.create_table('gameshow_event_contestants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['gameshow.event'], null=False)),
            ('contestant', models.ForeignKey(orm['gameshow.contestant'], null=False))
        ))
        db.create_unique('gameshow_event_contestants', ['event_id', 'contestant_id'])


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
            'result': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'gameshow.gameshow': {
            'Meta': {'object_name': 'Gameshow'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'season': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['gameshow']
