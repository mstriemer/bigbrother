from django import forms

from gameshow.models import Prediction

class PredictionForm(forms.ModelForm):
    class Meta:
        model = Prediction
        fields = ('contestant',)
