from django.urls import path
from . import views
from .views import (
    Conferenceliste,
    ConferenceDetail,
    AddConference,
    UpdateConference,
    DeleteConference
)
from .views import ListSubmissions
from .views import DetailSubmission, AddSubmission, UpdateSubmission


urlpatterns = [
    # La page par défaut /conferences/ affiche directement la liste
    path("", Conferenceliste.as_view(), name="conference_liste"),

    # Détails d'une conférence
    path("details/<int:pk>/", ConferenceDetail.as_view(), name="conference_details"),
    path("add/", AddConference.as_view(), name="add_conference"),  # <-- nouvelle route
    path("update/<int:pk>/", UpdateConference.as_view(), name="update_conference"),  # <-- nouvelle rou
    #  path("edit/<int:pk>/", UpdateConference.as_view(), name="addconference"), hedha kn chnestaaml page wahda
    path("delete/<int:pk>/", DeleteConference.as_view(), name="delete_conference"),  # <-- nouvelle route
   path("submissions/add/", AddSubmission.as_view(), name="add_submission"),
path("submissions/update/<str:pk>/", UpdateSubmission.as_view(), name="update_submission"),

     path("submissions/", ListSubmissions.as_view(), name="list_submissions"),
    path("submissions/<int:conference_id>/", ListSubmissions.as_view(), name="conference_submissions"),
    path("submissions/<str:pk>/", DetailSubmission.as_view(), name="detail_submission"),

 
   
]


