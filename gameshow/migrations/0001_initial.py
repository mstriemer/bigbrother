# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Gameshow'
        db.create_table('gameshow_gameshow', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('season', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('gameshow', ['Gameshow'])

        # Adding model 'Contestant'
        db.create_table('gameshow_contestant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('gameshow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gameshow.Gameshow'])),
        ))
        db.send_create_signal('gameshow', ['Contestant'])

        # Adding model 'Event'
        db.create_table('gameshow_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gameshow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gameshow.Gameshow'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('gameshow', ['Event'])

        # Adding M2M table for field contestants on 'Event'
        db.create_table('gameshow_event_contestants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['gameshow.event'], null=False)),
            ('contestant', models.ForeignKey(orm['gameshow.contestant'], null=False))
        ))
        db.create_unique('gameshow_event_contestants', ['event_id', 'contestant_id'])


    def backwards(self, orm):
        
        # Deleting model 'Gameshow'
        db.delete_table('gameshow_gameshow')

        # Deleting model 'Contestant'
        db.delete_table('gameshow_contestant')

        # Deleting model 'Event'
        db.delete_table('gameshow_event')

        # Removing M2M table for field contestants on 'Event'
        db.delete_table('gameshow_event_contestants')


    models = {
        'gameshow.contestant': {
            'Meta': {'object_name': 'Contestant'},
            'gameshow': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gameshow.Gameshow']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'gameshow.event': {
            'Meta': {'object_name': 'Event'},
            'contestants': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['gameshow.Contestant']", 'symmetrical': 'False'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'gameshow': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gameshow.Gameshow']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'gameshow.gameshow': {
            'Meta': {'object_name': 'Gameshow'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'season': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['gameshow']
