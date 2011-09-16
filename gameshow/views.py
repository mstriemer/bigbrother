from datetime import datetime

from django.views.generic import ListView, DetailView
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from gameshow.models import Gameshow, Contestant, Event, UserPrediction, \
                            UserPredictionChoice, Prediction, Team
from gameshow.forms import UserPredictionFormSet, UserPredictionChoiceForm, \
                            TeamFormSet

@login_required
def dashboard(request):
    gameshow = Gameshow.objects.get(pk=1)
    try:
        team = Team.objects.get(user=request.user)
    except Team.DoesNotExist:
        team = Team.objects.create(user=request.user)
    team_form_set = TeamFormSet(instance=team) if team.is_editable else None
    user_points = gameshow.calculate_points().items()
    user_points.sort(key=lambda up: up[1], reverse=True)
    predictions = []
    for prediction in Prediction.objects.all().order_by('-event__date'):
        try:
            predictions.append((prediction,
                prediction.userprediction_set.get(user=request.user)))
        except UserPrediction.DoesNotExist:
            predictions.append((prediction,
                UserPrediction.objects.create(
                user=request.user, prediction=prediction)))
    return render_to_response('gameshow/dashboard.html',
        {'gameshow': gameshow, 'user_points': user_points,
        'predictions': predictions, 'team': team,
        'team_form_set': team_form_set},
        context_instance=RequestContext(request))

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
    try:
        team = Team.objects.get(user=request.user)
    except Team.DoesNotExist:
        team = Team.objects.create(user=request.user)
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
    predictions = Prediction.objects.order_by('-event__date_performed').select_related()
    users = User.objects.all()
    return render_to_response('gameshow/points_detail.html',
            {'predictions': predictions, 'users': users},
            context_instance=RequestContext(request))
