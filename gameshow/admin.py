from django.contrib import admin

from gameshow.models import Gameshow, Contestant, Event, EventContestant, \
                            UserPrediction, Prediction, UserPredictionChoice, \
                            PredictionMatch, Team, TeamMembership


class EventContestantInline(admin.TabularInline):
    model = EventContestant
    extra = 0
    exclude = ('result',)


class EventInline(admin.TabularInline):
    model = Event
    extra = 1


class PredictionInline(admin.TabularInline):
    model = Prediction
    extra = 0


class PredictionMatchInline(admin.TabularInline):
    model = PredictionMatch
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'event_contestant':
            # FIXME: This is a horrible hack - Mk 28-07-2011
            try:
                pk = int(request.path.split('/')[-2])
                kwargs['queryset'] = Prediction.objects.get(
                        pk=pk).event.eventcontestant_set.order_by('contestant__name')
            except ValueError:
                pass
        return super(PredictionMatchInline, self).formfield_for_foreignkey(
                db_field, request, **kwargs)


class UserPredictionInline(admin.TabularInline):
    model = UserPrediction
    extra = 0


class UserPredictionChoiceInline(admin.TabularInline):
    model = UserPredictionChoice
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'event_contestant':
            # FIXME: This is a horrible hack - Mk 28-07-2011
            try:
                pk = int(request.path.split('/')[-2])
                kwargs['queryset'] = UserPrediction.objects.get(
                        pk=pk).prediction.event.eventcontestant_set.order_by(
                        'contestant__name')
            except ValueError:
                pass
        return super(UserPredictionChoiceInline, self).formfield_for_foreignkey(
                db_field, request, **kwargs)


class TeamMembershipInline(admin.TabularInline):
    model = TeamMembership
    extra = 4
    max_num = 4


class TeamAdmin(admin.ModelAdmin):
    list_display = ('user',)
    inlines = (TeamMembershipInline,)


class GameshowAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = (EventInline,)


class ContestantAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')
    inlines = (EventContestantInline,)


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    inlines = (EventContestantInline, PredictionInline)


class EventContestantAdmin(admin.ModelAdmin):
    list_display = ('event', 'contestant')
    exclude = ('result',)


class UserPredictionAdmin(admin.ModelAdmin):
    list_display = ('prediction', 'user')
    fields = ('prediction', 'user')
    inlines = (UserPredictionChoiceInline,)


class PredictionAdmin(admin.ModelAdmin):
    list_display = ('event', 'description', 'number_of_choices',
        'can_match_team')
    inlines = (PredictionMatchInline, UserPredictionInline,)
    list_editable = ('can_match_team',)


admin.site.register(Gameshow, GameshowAdmin)
admin.site.register(Contestant, ContestantAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventContestant, EventContestantAdmin)
admin.site.register(UserPrediction, UserPredictionAdmin)
admin.site.register(Prediction, PredictionAdmin)
admin.site.register(Team, TeamAdmin)
