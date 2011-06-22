from django.contrib import admin

from gameshow.models import Gameshow, Contestant, Event, EventContestant, \
                            Prediction


class EventContestantInline(admin.TabularInline):
    model = EventContestant
    extra = 1


class EventInline(admin.TabularInline):
    model = Event
    extra = 1


class PredictionInline(admin.TabularInline):
    model = Prediction
    extra = 1


class GameshowAdmin(admin.ModelAdmin):
    list_display = ('name', 'season')
    inlines = (EventInline,)


class ContestantAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')
    inlines = (EventContestantInline,)


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    inlines = (EventContestantInline, PredictionInline)


class EventContestantAdmin(admin.ModelAdmin):
    list_display = ('event', 'contestant', 'place', 'result')
    list_editable = ('place', 'result')


class PredictionAdmin(admin.ModelAdmin):
    list_display = ('event', 'contestant', 'user', 'description')

admin.site.register(Gameshow, GameshowAdmin)
admin.site.register(Contestant, ContestantAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventContestant, EventContestantAdmin)
admin.site.register(Prediction, PredictionAdmin)
