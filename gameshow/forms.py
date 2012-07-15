from django import forms
from django.forms.models import inlineformset_factory

from gameshow.models import Team, TeamMembership, Contestant, Gameshow


class TeamMembershipForm(forms.ModelForm):
    contestant = forms.ModelChoiceField(
            queryset=Contestant.objects.filter(
                gameshow=Gameshow.objects.current(), state='active'),
            widget=forms.Select(attrs={'class': 'span2'}))

    class Meta:
        model = TeamMembership


def _team_form_set_clean(self):
    """Don't allow the same team member multiple times"""
    if any(self.errors):
        return  # Don't validate if there are other errors
    contestants = []
    error_msg = None
    for form in self.forms:
        contestant = form.cleaned_data['contestant']
        if contestant in contestants:
            error_msg = "You may only add a contestant to your team once."
            form._errors['contestant'] = form.error_class([error_msg])
        else:
            contestants.append(contestant)
    if error_msg:
        raise forms.ValidationError(error_msg)

TeamFormSet = inlineformset_factory(Team, TeamMembership, can_delete=False,
        extra=4, max_num=4, form=TeamMembershipForm)
TeamFormSet.clean = _team_form_set_clean
