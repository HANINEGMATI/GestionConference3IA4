from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Conference, Submission
from .form import ConferenceForm
from django.core.exceptions import PermissionDenied



# ✅ Liste de toutes les conférences
class Conferenceliste(ListView):
    model = Conference
    template_name = "conference/liste.html"
    context_object_name = "conferences"
    queryset = Conference.objects.all().order_by('start_date')


# ✅ Détail d’une conférence
class ConferenceDetail(DetailView):
    model = Conference
    template_name = "conference/detail.html"
    context_object_name = "conference"


# ✅ Ajouter une conférence
class AddConference(LoginRequiredMixin, CreateView):
    model = Conference
    form_class = ConferenceForm
    template_name = "conference/add_conference.html"
    success_url = reverse_lazy('conference_liste')


# ✅ Modifier une conférence
class UpdateConference(LoginRequiredMixin, UpdateView):
    model = Conference
    form_class = ConferenceForm
    template_name = "conference/update_conference.html"
    success_url = reverse_lazy('conference_liste')


# ✅ Supprimer une conférence
class DeleteConference(LoginRequiredMixin, DeleteView):
    model = Conference
    template_name = "conference/delete_conference.html"
    success_url = reverse_lazy('conference_liste')


# ✅ Liste des soumissions
class ListSubmissions(ListView):
    model = Submission
    template_name = "conference/list_submissions.html"
    context_object_name = "submissions"

    def get_queryset(self):
        conference_id = self.kwargs.get("conference_id")
        if conference_id:
            return Submission.objects.filter(conference_id=conference_id)
        return Submission.objects.all().order_by('-submission_date')


# ✅ Détail d’une soumission
class DetailSubmission(LoginRequiredMixin, DetailView):
    model = Submission
    template_name = "conference/detail_submission.html"
    context_object_name = "submission"
    pk_url_kwarg = "pk"

class AddSubmission(LoginRequiredMixin, CreateView):
    model = Submission
    template_name = "conference/add_submission.html"
    fields = ["title", "abstract", "keywords", "file", "conference_id"]  # champs corrects
    success_url = reverse_lazy("list_submissions")

    def form_valid(self, form):
        # Associer l'utilisateur connecté avant validation
        form.instance.user_id = self.request.user
        return super().form_valid(form)

class UpdateSubmission(LoginRequiredMixin, UpdateView):
    model = Submission
    fields = ['title', 'abstract', 'keywords', 'file']
    template_name = 'conference/update_submission.html'
    success_url = reverse_lazy('list_submissions')
    pk_url_kwarg = 'pk'

    def dispatch(self, request, *args, **kwargs):
        """Empêche la modification si la soumission est Accepted ou Rejected"""
        submission = self.get_object()
        if submission.status in ["Accepted", "Rejected"]:
            raise PermissionDenied("Cette soumission ne peut pas être modifiée car elle a été acceptée ou rejetée.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Assure que l'utilisateur reste le même
        form.instance.user_id = self.request.user
        return super().form_valid(form)
