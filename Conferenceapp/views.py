from django.shortcuts import render
from .models import Conference
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from .form import ConferenceForm

def all_conferences(req):
    conferences = Conference.objects.all()
    return render(req, 'conference/liste.html', {"liste": conferences})

class Conferenceliste(ListView):
    model = Conference
    template_name = "conference/liste.html"   # fichier template utilisé
    context_object_name = "conferences"       # variable disponible dans le template
    queryset = Conference.objects.all().order_by('start_date')

class ConferenceDetail(DetailView):               # renamed pour la convention CamelCase
    model = Conference
    template_name = "conference/detail.html"     # corrigé: 'details.html'
    context_object_name = "conference"
class AddConference(CreateView):
    model = Conference
    form_class = ConferenceForm  # <-- Utilise uniquement le ModelForm
    template_name = "conference/add_conference.html"
    success_url = reverse_lazy('conference_liste')

class UpdateConference(UpdateView):
    model = Conference
    form_class = ConferenceForm  # <-- uniquement le ModelForm
    template_name = "conference/update_conference.html"
    success_url = reverse_lazy('conference_liste')

class DeleteConference(DeleteView):
    model = Conference
    template_name = "conference/delete_conference.html"  # template de confirmation
    success_url = reverse_lazy('conference_liste')