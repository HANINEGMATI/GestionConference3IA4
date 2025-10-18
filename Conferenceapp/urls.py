from django.urls import path
from . import views
from .views import (
    Conferenceliste,
    ConferenceDetail,
    AddConference,
    UpdateConference,
    DeleteConference
)

urlpatterns = [
    # La page par défaut /conferences/ affiche directement la liste
    path("", Conferenceliste.as_view(), name="conference_liste"),

    # Détails d'une conférence
    path("details/<int:pk>/", ConferenceDetail.as_view(), name="conference_details"),
    path("add/", AddConference.as_view(), name="add_conference"),  # <-- nouvelle route
    path("update/<int:pk>/", UpdateConference.as_view(), name="update_conference"),  # <-- nouvelle rou
    path("delete/<int:pk>/", DeleteConference.as_view(), name="delete_conference"),  # <-- nouvelle route
]