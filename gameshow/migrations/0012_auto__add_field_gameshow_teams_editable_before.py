# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Gameshow.teams_editable_before'
        db.add_column(u'gameshow_gameshow', 'teams_editable_before',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 2, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Gameshow.teams_editable_before'
        db.delete_column(u'gameshow_gameshow', 'teams_editable_before')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'gameshow.contestant': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Contestant'},
            'gameshow': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gameshow.Gameshow']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        u'gameshow.event': {
            'Meta': {'object_name': 'Event'},
            'contestants': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['gameshow.Contestant']", 'through': u"orm['gameshow.EventContestant']", 'symmetrical': 'False'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_performed': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'gameshow': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gameshow.Gameshow']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'gameshow.eventcontestant': {
            'Meta': {'object_name': 'EventContestant'},
            'contestant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gameshow.Contestant']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gameshow.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'gameshow.gameshow': {
            'Meta': {'object_name': 'Gameshow'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'teams_editable_before': ('django.db.models.fields.DateTimeField', [], {}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'})
        },
        u'gameshow.prediction': {
            'Meta': {'object_name': 'Prediction'},
            'can_match_team': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gameshow.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matches': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['gameshow.EventContestant']", 'through': u"orm['gameshow.PredictionMatch']", 'symmetrical': 'False'}),
            'number_of_choices': ('django.db.models.fields.IntegerField', [], {}),
            'points': ('django.db.models.fields.IntegerField', [], {})
        },
        u'gameshow.predictionmatch': {
            'Meta': {'object_name': 'PredictionMatch'},
            'event_contestant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gameshow.EventContestant']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prediction': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gameshow.Prediction']"})
        },
        u'gameshow.team': {
            'Meta': {'object_name': 'Team'},
            'contestants': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['gameshow.Contestant']", 'through': u"orm['gameshow.TeamMembership']", 'symmetrical': 'False'}),
            'gameshow': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gameshow.Gameshow']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'gameshow.teammembership': {
            'Meta': {'object_name': 'TeamMembership'},
            'contestant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gameshow.Contestant']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gameshow.Team']"})
        },
        u'gameshow.userprediction': {
            'Meta': {'object_name': 'UserPrediction'},
            'event_contestants': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['gameshow.EventContestant']", 'through': u"orm['gameshow.UserPredictionChoice']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prediction': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gameshow.Prediction']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'gameshow.userpredictionchoice': {
            'Meta': {'object_name': 'UserPredictionChoice'},
            'event_contestant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gameshow.EventContestant']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_prediction': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gameshow.UserPrediction']"})
        }
    }

    complete_apps = ['gameshow']