# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'EventPrediction'
        db.delete_table('gameshow_eventprediction')

        # Adding model 'UserPrediction'
        db.create_table('gameshow_userprediction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('prediction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gameshow.Prediction'])),
            ('event_contestant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gameshow.EventContestant'])),
        ))
        db.send_create_signal('gameshow', ['UserPrediction'])

        # Deleting field 'Prediction.event_contestant'
        db.delete_column('gameshow_prediction', 'event_contestant_id')

        # Deleting field 'Prediction.event_prediction'
        db.delete_column('gameshow_prediction', 'event_prediction_id')

        # Deleting field 'Prediction.user'
        db.delete_column('gameshow_prediction', 'user_id')

        # Adding field 'Prediction.event'
        db.add_column('gameshow_prediction', 'event', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['gameshow.Event']), keep_default=False)

        # Adding field 'Prediction.result'
        db.add_column('gameshow_prediction', 'result', self.gf('django.db.models.fields.IntegerField')(default=1), keep_default=False)

        # Adding field 'Prediction.points'
        db.add_column('gameshow_prediction', 'points', self.gf('django.db.models.fields.IntegerField')(default=1), keep_default=False)

        # Adding field 'Prediction.description'
        db.add_column('gameshow_prediction', 'description', self.gf('django.db.models.fields.CharField')(default=1, max_length=100), keep_default=False)


    def backwards(self, orm):
        
        # Adding model 'EventPrediction'
        db.create_table('gameshow_eventprediction', (
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gameshow.Event'])),
            ('result', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('points', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('gameshow', ['EventPrediction'])

        # Deleting model 'UserPrediction'
        db.delete_table('gameshow_userprediction')

        # Adding field 'Prediction.event_contestant'
        db.add_column('gameshow_prediction', 'event_contestant', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['gameshow.EventContestant']), keep_default=False)

        # Adding field 'Prediction.event_prediction'
        db.add_column('gameshow_prediction', 'event_prediction', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['gameshow.EventPrediction']), keep_default=False)

        # Adding field 'Prediction.user'
        db.add_column('gameshow_prediction', 'user', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User']), keep_default=False)

        # Deleting field 'Prediction.event'
        db.delete_column('gameshow_prediction', 'event_id')

        # Deleting field 'Prediction.result'
        db.delete_column('gameshow_prediction', 'result')

        # Deleting field 'Prediction.points'
        db.delete_column('gameshow_prediction', 'points')

        # Deleting field 'Prediction.description'
        db.delete_column('gameshow_prediction', 'description')


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
        'gameshow.gameshow': {
            'Meta': {'object_name': 'Gameshow'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'gameshow.prediction': {
            'Meta': {'object_name': 'Prediction'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gameshow.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points': ('django.db.models.fields.IntegerField', [], {}),
            'result': ('django.db.models.fields.IntegerField', [], {})
        },
        'gameshow.userprediction': {
            'Meta': {'object_name': 'UserPrediction'},
            'event_contestant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gameshow.EventContestant']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prediction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gameshow.Prediction']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['gameshow']
