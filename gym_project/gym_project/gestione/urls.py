
from django.urls import path
from .views import *

app_name = "gestione"

urlpatterns = [
    path("", gestione_home, name="home"),
    path("listadiscipline/", DisciplinaListView.as_view(),name="listadiscipline"),
    path("ricerca_discipline/", search_disciplina, name="cercadisciplina"),
    path("ricerca_discipline/<str:sstring>/<str:where>/", DisciplinaRicercaView.as_view(), name="ricerca_disciplina_risultati"),
    path("listacorsi/<int:pk>", CorsoListView.as_view(),name="listacorsi"),
    path("ricerca_corsi/", search_corso, name="cercacorso"),
    path("ricerca_corsi/<str:sstring>/<str:where>/", CorsoRicercaView.as_view(), name="ricerca_corso_risultati"),
    path("prenotazione/<int:pk>/", prenotazione, name="prenotazione"),
    path("situation/", my_situation, name="situation"),
    path("disdetta/<int:pk>/", disdetta, name="disdetta"),

    path("situationg/", GymSituationView.as_view(),name="situationg"),
    path("detailg/<pk>/", GymDetailView.as_view(), name="detailg"),
    path("crea_disciplina/",CreateDisciplinaView.as_view(),name="creadisciplina"),
    path("crea_corso/",CreateCorsoView.as_view(),name="creacorso"),

    path("ricerca/gethint/", get_hint, name="get_hint")
]