from django.forms import ModelForm
from django.forms.models import BaseModelFormSet, inlineformset_factory

from gameshow.models import UserPrediction, UserPredictionChoice, \
                            EventContestant, Team, TeamMembership

UserPredictionFormSet = inlineformset_factory(UserPrediction,
    UserPredictionChoice, can_delete=False)


TeamFormSet = inlineformset_factory(Team, TeamMembership, can_delete=False,
        extra=4, max_num=4)

class UserPredictionChoiceForm(ModelForm):
    class Meta:
        model = UserPredictionChoice
        fields = ('event_contestant',)

    def __init__(self, *args, **kwargs):
        super(UserPredictionChoiceForm, self).__init__(*args, **kwargs)
        self.fields['event_contestant'].queryset = \
            EventContestant.objects.filter(
            event=kwargs['instance'].user_prediction.prediction.event)


class UserPredictionForm(ModelForm):
    class Meta:
        model = UserPrediction
        fields = ('event_contestants',)

    def __init__(self, *args, **kwargs):
        super(UserPredictionForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            self.fields['event_contestants'].queryset = \
                EventContestant.objects.filter(
                event=kwargs['instance'].prediction.event)
