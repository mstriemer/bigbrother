from django.forms import ModelForm, ModelChoiceField, Select
from django.forms.models import inlineformset_factory

from gameshow.models import Team, TeamMembership, Contestant, Gameshow


class TeamMembershipForm(ModelForm):
    contestant = ModelChoiceField(
            queryset=Contestant.objects.filter(
                gameshow=Gameshow.objects.current(), state='active'),
            widget=Select(attrs={'class': 'span2'}))

    class Meta:
        model = TeamMembership


TeamFormSet = inlineformset_factory(Team, TeamMembership, can_delete=False,
        extra=4, max_num=4, form=TeamMembershipForm)
