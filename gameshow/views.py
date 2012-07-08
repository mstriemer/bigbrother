from datetime import datetime

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from gameshow.models import Gameshow, UserPrediction
from gameshow.forms import TeamFormSet

@login_required
def dashboard(request):
    gameshow = Gameshow.objects.current()
    team, created = gameshow.team_set.get_or_create(user=request.user)
    team_form_set = TeamFormSet(instance=team) if team.is_editable else None
    user_points = gameshow.calculate_points().items()
    user_points.sort(key=lambda up: up[1], reverse=True)
    predictions = []
    for prediction in gameshow.prediction_set.order_by('-event__date'):
        user_prediction, created = prediction.userprediction_set.get_or_create(
                user=request.user)
        predictions.append((prediction, user_prediction))
    return render_to_response('gameshow/dashboard.html',
        {'gameshow': gameshow, 'user_points': user_points,
        'predictions': predictions, 'team': team,
        'team_form_set': team_form_set},
        context_instance=RequestContext(request))

@login_required
def prediction_detail(request, pk):
    prediction = UserPrediction.objects.get(pk=pk, user=request.user)
    if prediction.prediction.event.date > datetime.now():
        form = prediction.as_form(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, '{0} prediction successfully'
                ' updated'.format(prediction.prediction.event.name))
            return redirect('/bigbrother/')
        else:
            return render_to_response('gameshow/prediction_edit.html',
                {'form': form, 'prediction': prediction},
                context_instance=RequestContext(request))
    return render_to_response('gameshow/prediction_detail.html',
        {'prediction': prediction}, context_instance=RequestContext(request))

@login_required
def team_detail(request):
    gameshow = Gameshow.objects.current()
    team, created = gameshow.team_set.get_or_create(user=request.user)
    if team.is_editable:
        form_set = TeamFormSet(request.POST or None, instance=team)
        if form_set.is_valid():
            form_set.save()
            messages.success(request, 'Your team was successfully updated')
            return redirect('/bigbrother/')
    else:
        form_set = None
    return render_to_response('gameshow/team_detail.html', {'team': team,
        'form_set': form_set}, context_instance=RequestContext(request))

@login_required
def points_detail(request):
    gameshow = Gameshow.objects.current()
    predictions = gameshow.prediction_set.order_by('event__date_performed'
            ).filter(event__date_performed__lte=datetime.today())
    users = gameshow.users.all()
    everything = []
    user_points = dict((u, 0) for u in users)
    for prediction in predictions:
        prediction_user_points = dict((u, {'prediction_points': 0,
                'team_points': 0}) for u in users)
        for pmatch in prediction.matching_user_predictions.all():
            prediction_user_points[pmatch.user]['prediction_points'] += \
                    prediction.points
        for tmatch in prediction.matching_teams.all():
            prediction_user_points[tmatch.user]['team_points'] += \
                    prediction.points / 2
        prediction_row = {
            'prediction': {
                'event_name': prediction.event.name,
                'event_date': prediction.event.date
            },
            'users': {}
        }
        for user, points in prediction_user_points.items():
            event_points = points['prediction_points'] + \
                    points['team_points']
            points.update({'event_points': event_points,
                'old_total_points': user_points[user]})
            user_points[user] += event_points
            points.update({'new_total_points': user_points[user]})
            prediction_row['users'][user] = points
        everything.append(prediction_row)
    everything.reverse()
    return render_to_response('gameshow/points_detail.html',
            {'everything': everything},
            context_instance=RequestContext(request))
