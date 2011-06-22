from django.views.generic import ListView, DetailView
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages


from gameshow.models import Gameshow, Contestant, Event, Prediction
from gameshow.forms import PredictionForm

gameshow_list = ListView.as_view(model=Gameshow,
    context_object_name='gameshow_list')

gameshow_detail = DetailView.as_view(model=Gameshow,
    context_object_name='gameshow')

contestant_detail = DetailView.as_view(model=Contestant,
    context_object_name='contestant')

event_detail = DetailView.as_view(model=Event, context_object_name='event')

prediction_list = ListView.as_view(model=Prediction,
    context_object_name='prediction_list')

def prediction_list(request):
    predictions = Prediction.objects.all()[:10]
    pfs = [(p, PredictionForm(instance=p)) for p in predictions]
    return render_to_response('gameshow/prediction_list.html',
        {'prediction_list': pfs}, context_instance=RequestContext(request))

def prediction_detail(request, pk):
    prediction = Prediction.objects.get(pk=pk)
    if request.method == 'POST':
        form = PredictionForm(request.POST, instance=prediction)
        if form.is_valid() and form.save():
            messages.success(request, 'Prediction successfully updated.')
            return redirect('gameshow.views.prediction_list')
    else:
        form = PredictionForm(instance=prediction)
    return render_to_response('gameshow/prediction_detail.html',
        {'prediction': prediction, 'form': form},
        context_instance=RequestContext(request))
