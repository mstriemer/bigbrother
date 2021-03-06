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
        ))
        db.send_create_signal('gameshow', ['Gameshow'])

        # Adding model 'Contestant'
        db.create_table('gameshow_contestant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gameshow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gameshow.Gameshow'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('gameshow', ['Contestant'])

        # Adding model 'Event'
        db.create_table('gameshow_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gameshow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gameshow.Gameshow'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_performed', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('gameshow', ['Event'])

        # Adding model 'EventContestant'
        db.create_table('gameshow_eventcontestant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gameshow.Event'])),
            ('contestant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gameshow.Contestant'])),
            ('result', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('gameshow', ['EventContestant'])

        # Adding model 'EventPrediction'
        db.create_table('gameshow_eventprediction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gameshow.Event'])),
            ('result', self.gf('django.db.models.fields.IntegerField')()),
            ('points', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('gameshow', ['EventPrediction'])

        # Adding model 'Prediction'
        db.create_table('gameshow_prediction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('event_prediction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gameshow.EventPrediction'])),
            ('event_contestant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gameshow.EventContestant'])),
        ))
        db.send_create_signal('gameshow', ['Prediction'])


    def backwards(self, orm):
        
        # Deleting model 'Gameshow'
        db.delete_table('gameshow_gameshow')

        # Deleting model 'Contestant'
        db.delete_table('gameshow_contestant')

        # Deleting model 'Event'
        db.delete_table('gameshow_event')

        # Deleting model 'EventContestant'
        db.delete_table('gameshow_eventcontestant')

        # Deleting model 'EventPrediction'
        db.delete_table('gameshow_eventprediction')

        # Deleting model 'Prediction'
        db.delete_table('gameshow_prediction')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'gameshow.contestant': {
            'Meta': {'object_name': 'Contestant'},
            'gameshow': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gameshow.Gameshow']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'gameshow.event': {
            'Meta': {'object_name': 'Event'},
            'contestants': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['gameshow.Contestant']", 'through': "orm['gameshow.EventContestant']", 'symmetrical': 'False'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_performed': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'gameshow': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gameshow.Gameshow']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'gameshow.eventcontestant': {
            'Meta': {'object_name': 'EventContestant'},
            'contestant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gameshow.Contestant']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gameshow.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'gameshow.eventprediction': {
            'Meta': {'object_name': 'EventPrediction'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gameshow.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points': ('django.db.models.fields.IntegerField', [], {}),
            'result': ('django.db.models.fields.IntegerField', [], {})
        },
        'gameshow.gameshow': {
            'Meta': {'object_name': 'Gameshow'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'gameshow.prediction': {
            'Meta': {'object_name': 'Prediction'},
            'event_contestant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gameshow.EventContestant']"}),
            'event_prediction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gameshow.EventPrediction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['gameshow']
