
from django.urls import path
from .views import *

app_name = "gestione"

urlpatterns = [
    path("", gestione_home, name="home"),
    path("listacorsi/", CorsoListView.as_view(),name="listacorsi"),
    path("ricerca/", search, name="cercacorso"),
    path("ricerca/<str:sstring>/<str:where>/", CorsoRicercaView.as_view(), name="ricerca_risultati"),
    path("prenotazione/<pk>/", prenotazione, name="prenotazione"),
    path("situation/", my_situation, name="situation"),
    path("restituzione/<pk>/", RestituisciView.as_view(), name="restituzione"),

    path("situationb/", GymSituationView.as_view(),name="situationb"),
    path("detailb/<pk>/", GymDetailView.as_view(), name="detailb"),
    path("crea_corso/",CreateCorsoView.as_view(),name="creacorso"),
    path("crea_occorrenza/",CreateOccorrenzaView.as_view(),name="creaoccorrenza"),

    path("ricerca/gethint/", get_hint, name="get_hint")
]