import json
from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from rest_framework import permissions, serializers, viewsets

from gameshow.models import Contestant, Event, EventContestant, Gameshow, Team, UserPrediction
from gameshow.forms import TeamForm, TeamFormSet


def redirect_to_current(request):
    gameshow = Gameshow.objects.current()
    return redirect(
        reverse('gameshow.views.dashboard', args=[gameshow.slug]))


def format_predictions(predictions, user):
    def format_prediction(prediction):
        user_prediction, created = prediction.userprediction_set.get_or_create(
            user=user)
        return (prediction, user_prediction)
    return [format_prediction(prediction) for prediction in predictions]


@login_required
def past_predictions(request, gameshow_slug):
    gameshow = Gameshow.objects.get(slug=gameshow_slug)
    team, created = gameshow.team_set.get_or_create(user=request.user)
    user_points = gameshow.calculate_points().items()
    user_points.sort(key=lambda up: up[1], reverse=True)
    predictions = format_predictions(gameshow.prediction_set.filter(
        event__date_performed__lte=datetime.now()).order_by(
        '-event__date_performed', '-event__date'), request.user)
    return render_to_response(
        'gameshow/past_predictions.html',
        {'gameshow': gameshow, 'predictions': predictions, 'team': team,
         'user_points': user_points},
        context_instance=RequestContext(request))


@login_required
def dashboard(request, gameshow_slug):
    try:
        gameshow = Gameshow.objects.get(slug=gameshow_slug)
    except Gameshow.DoesNotExist:
        return redirect_to_current(request)
    team, created = gameshow.team_set.get_or_create(user=request.user)
    if team.is_editable:
        team_form_set = TeamFormSet(instance=team)
        team_form = TeamForm(instance=team)
    else:
        team_form_set = None
        team_form = None
    user_points = gameshow.calculate_points().items()
    user_points.sort(key=lambda up: up[1], reverse=True)
    now = datetime.now()
    upcoming_predictions = format_predictions(gameshow.prediction_set.filter(
        event__date_performed__gte=now).order_by(
        'event__date_performed', 'event__date'), request.user)
    past_predictions = format_predictions(gameshow.prediction_set.filter(
        event__date_performed__lte=now,
        event__date_performed__gte=now - timedelta(days=7)).order_by(
        '-event__date_performed', '-event__date'), request.user)
    return render_to_response(
        'gameshow/dashboard.html',
        {'gameshow': gameshow, 'user_points': user_points,
         'upcoming_predictions': upcoming_predictions,
         'past_predictions': past_predictions,
         'team': team, 'team_form': team_form, 'team_form_set': team_form_set},
        context_instance=RequestContext(request))


@login_required
def prediction_detail(request, gameshow_slug, pk):
    gameshow = Gameshow.objects.get(slug=gameshow_slug)
    prediction = UserPrediction.objects.get(pk=pk, user=request.user)
    if prediction.is_editable:
        form = prediction.as_form(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                '{0} prediction successfully'
                ' updated'.format(prediction.prediction.event.name))
            return redirect(
                reverse('gameshow.views.dashboard', args=[gameshow.slug]))
        else:
            return render_to_response(
                'gameshow/prediction_form.html',
                {'form': form, 'prediction': prediction, 'gameshow': gameshow},
                context_instance=RequestContext(request))
    return redirect(reverse('gameshow.views.dashboard', args=[gameshow.slug]))


@login_required
def team_detail(request, gameshow_slug):
    gameshow = Gameshow.objects.get(slug=gameshow_slug)
    team, created = gameshow.team_set.get_or_create(user=request.user)
    if team.is_editable:
        form_set = TeamFormSet(request.POST or None, instance=team)
        team_form = TeamForm(request.POST or None, instance=team)
        if form_set.is_valid() and team_form.is_valid():
            form_set.save()
            team_form.save()
            messages.success(request, 'Your team was successfully updated')
            return redirect(
                reverse('gameshow.views.dashboard', args=[gameshow.slug]))
    else:
        form_set = None
    return render_to_response(
        'gameshow/team_detail.html',
        {'team': team, 'form_set': form_set, 'gameshow': gameshow},
        context_instance=RequestContext(request))


def rules(request):
    gameshow = Gameshow.objects.current()
    return render_to_response(
        'gameshow/bigbrother_rules.html',
        {'gameshow': gameshow}, context_instance=RequestContext(request))


@login_required
def graph(request, gameshow_slug):
    return render_to_response(
        'gameshow/graphs.html',
        context_instance=RequestContext(request))


@login_required
def points_detail(request, gameshow_slug):
    gameshow = Gameshow.objects.get(slug=gameshow_slug)
    everything, user_points = all_user_points(gameshow)
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
    return render_to_response(
        'gameshow/points_detail.html',
        {'everything': everything, 'totals': user_points,
         'max_points': max_points, 'winners': winners, 'gameshow': gameshow},
        context_instance=RequestContext(request))


def all_user_points(gameshow):
    predictions = gameshow.prediction_set.order_by(
        'event__date_performed').filter(
            event__date_performed__lte=datetime.today())
    users = gameshow.users.all()
    everything = []
    user_points = dict((u, dict(total=0, team=0, prediction=0)) for u in users)
    for prediction in predictions:
        prediction_user_points = dict(
            (u, {'prediction_points': 0, 'team_points': 0})
            for u in users)
        for pmatch in prediction.matching_user_predictions.all():
            prediction_user_points[pmatch.user]['prediction_points'] += (
                prediction.points)
            user_points[pmatch.user]['prediction'] += prediction.points
        for tmatch in prediction.matching_teams.all():
            prediction_user_points[tmatch.user]['team_points'] += (
                prediction.points / 2)
            user_points[tmatch.user]['team'] += prediction.points / 2
        prediction_row = {
            'prediction': {
                'event_name': prediction.event.name,
                'event_date': prediction.event.date
            },
            'users': {}
        }
        for user, points in prediction_user_points.items():
            event_points = points['prediction_points'] + (
                points['team_points'])
            points.update({
                'event_points': event_points,
                'old_total_points': user_points[user]['total']})
            user_points[user]['total'] += event_points
            points.update({'new_total_points': user_points[user]['total']})
            prediction_row['users'][user] = points
        everything.append(prediction_row)
    return reversed(everything), user_points


@login_required
def teams(request, gameshow_slug):
    gameshow = get_object_or_404(Gameshow, slug=gameshow_slug)
    return render_to_response(
        'gameshow/teams.html',
        {'gameshow': gameshow},
        context_instance=RequestContext(request))


@login_required
def new_event(request, gameshow_slug):
    gameshow = get_object_or_404(Gameshow, slug=gameshow_slug)
    return render_to_response('gameshow/new_event.html', {
        'gameshow': gameshow,
        'gameshow_data': json.dumps({
            'pk': gameshow.pk,
            'name': gameshow.name,
        }),
    }, context_instance=RequestContext(request))


class IsOwner(permissions.IsAuthenticated):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if super(IsOwner, self).has_object_permission(request, view, obj):
            # Write permissions are only allowed to the owner of the snippet.
            return obj.user == request.user
        else:
            return False


class GameshowViewSet(viewsets.ReadOnlyModelViewSet):
    model = Gameshow
    permission_classes = [permissions.IsAuthenticated]


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    model = Team
    permission_classes = [IsOwner]

    def get_queryset(self):
        queryset = super(TeamViewSet, self).get_queryset()
        gameshow_id = self.request.QUERY_PARAMS.get('gameshow_id')
        if gameshow_id:
            queryset = queryset.filter(gameshow_id=gameshow_id)
        return queryset


class ContestantViewSet(viewsets.ReadOnlyModelViewSet):
    model = Contestant
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    model = User
    permission_classes = [permissions.IsAuthenticated]


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['gameshow', 'name', 'date', 'date_performed', 'contestants',
                  'id']
        model = Event

    def create(self, validated_data):
        event = super(EventSerializer, self).create(validated_data)
        for contestant in event.gameshow.contestant_set.filter(state='active'):
            EventContestant.objects.create(event=event, contestant=contestant)
        return event


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        gameshow_pk = self.request.query_params.get('gameshow')
        if gameshow_pk:
            return self.queryset.filter(gameshow__pk=gameshow_pk)
        else:
            return super(EventViewSet, self).get_queryset()
