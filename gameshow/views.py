from datetime import datetime

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from gameshow.models import Gameshow, UserPrediction
from gameshow.forms import TeamFormSet

def redirect_to_current(request):
    gameshow = Gameshow.objects.current()
    return redirect(
        reverse('gameshow.views.dashboard', args=[gameshow.slug]))

@login_required
def dashboard(request, gameshow_slug):
    gameshow = Gameshow.objects.get(slug=gameshow_slug)
    team, created = gameshow.team_set.get_or_create(user=request.user)
    team_form_set = TeamFormSet(instance=team) if team.is_editable else None
    user_points = gameshow.calculate_points().items()
    user_points.sort(key=lambda up: up[1], reverse=True)
    predictions = []
    for prediction in gameshow.prediction_set.order_by(
            '-event__date_performed', '-event__date'):
        user_prediction, created = prediction.userprediction_set.get_or_create(
                user=request.user)
        predictions.append((prediction, user_prediction))
    return render_to_response('gameshow/dashboard.html',
        {'gameshow': gameshow, 'user_points': user_points,
        'predictions': predictions, 'team': team,
        'team_form_set': team_form_set, 'gameshow': gameshow},
        context_instance=RequestContext(request))

@login_required
def prediction_detail(request, gameshow_slug, pk):
    gameshow = Gameshow.objects.get(slug=gameshow_slug)
    prediction = UserPrediction.objects.get(pk=pk, user=request.user)
    if prediction.is_editable:
        form = prediction.as_form(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, '{0} prediction successfully'
                ' updated'.format(prediction.prediction.event.name))
            return redirect(
                reverse('gameshow.views.dashboard', args=[gameshow.slug]))
        else:
            return render_to_response('gameshow/prediction_form.html',
                {'form': form, 'prediction': prediction, 'gameshow': gameshow},
                context_instance=RequestContext(request))
    return redirect(reverse('gameshow.views.dashboard', args=[gameshow.slug]))

@login_required
def team_detail(request, gameshow_slug):
    gameshow = Gameshow.objects.get(slug=gameshow_slug)
    team, created = gameshow.team_set.get_or_create(user=request.user)
    if team.is_editable:
        form_set = TeamFormSet(request.POST or None, instance=team)
        if form_set.is_valid():
            form_set.save()
            messages.success(request, 'Your team was successfully updated')
            return redirect(
                reverse('gameshow.views.dashboard', args=[gameshow.slug]))
    else:
        form_set = None
    return render_to_response('gameshow/team_detail.html',
        {'team': team, 'form_set': form_set, 'gameshow': gameshow},
        context_instance=RequestContext(request))

def rules(request):
    gameshow = Gameshow.objects.current()
    return render_to_response('gameshow/bigbrother_rules.html',
        {'gameshow': gameshow}, context_instance=RequestContext(request))

@login_required
def points_detail(request, gameshow_slug):
    gameshow = Gameshow.objects.get(slug=gameshow_slug)
    predictions = gameshow.prediction_set.order_by('event__date_performed'
            ).filter(event__date_performed__lte=datetime.today())
    users = gameshow.users.all()
    everything = []
    user_points = dict((u, dict(total=0, team=0, prediction=0)) for u in users)
    for prediction in predictions:
        prediction_user_points = dict((u, {'prediction_points': 0,
                'team_points': 0}) for u in users)
        for pmatch in prediction.matching_user_predictions.all():
            prediction_user_points[pmatch.user]['prediction_points'] += \
                    prediction.points
            user_points[pmatch.user]['prediction'] += prediction.points
        for tmatch in prediction.matching_teams.all():
            prediction_user_points[tmatch.user]['team_points'] += \
                    prediction.points / 2
            user_points[tmatch.user]['team'] += prediction.points / 2
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
                'old_total_points': user_points[user]['total']})
            user_points[user]['total'] += event_points
            points.update({'new_total_points': user_points[user]['total']})
            prediction_row['users'][user] = points
        everything.append(prediction_row)
    everything.reverse()
    the_points = user_points.items()
    max_points = {}
    max_points['team'] = max(p['team'] for u, p in the_points)
    max_points['prediction'] = max(p['prediction'] for u, p in the_points)
    max_points['total'] = max(p['total'] for u, p in the_points)
    winners = {}
    most_points = dict(total=0, team=0, prediction=0)
    for user, points in the_points:
        for field in ('team', 'prediction'):
            if points[field] > most_points[field]:
                most_points[field] = points[field]
                winners[field] = user.first_name
    total_points = [(u, p['total']) for u, p in the_points]
    total_points.sort(key=lambda t: t[1])
    winners['first'] = total_points[-1][0].first_name
    winners['second'] = total_points[-2][0].first_name
    winners['third'] = total_points[-3][0].first_name
    return render_to_response('gameshow/points_detail.html',
        {'everything': everything, 'totals': user_points,
        'max_points': max_points, 'winners': winners, 'gameshow': gameshow},
        context_instance=RequestContext(request))
