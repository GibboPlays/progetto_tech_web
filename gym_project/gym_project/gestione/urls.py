
from django.urls import path
from .views import *

app_name = "gestione"

urlpatterns = [
    path("", gestione_home, name="home"),
    path("listadiscipline/", DisciplinaListView.as_view(),name="listadiscipline"),
    path("ricerca_discipline/", search_disciplina, name="cercadisciplina"),
    path("ricerca_discipline/<str:sstring>/<str:where>/", DisciplinaRicercaView.as_view(), name="ricerca_disciplina_risultati"),
    path("listacorsi/<int:pk>", CorsoListView.as_view(),name="listacorsi"),
    path("lista_corsi_giornalieri/", CorsoListDailyView.as_view(), name="lista_corsi_giornalieri"),
    path('lista_corsi_giornalieri/<str:data>/', CorsoListDailyView.as_view(), name='lista_corsi_giornalieri_data'),
    path("ricerca_corsi/", CorsoRicercaView.as_view(), name="ricerca_corso_risultati"),
    path("prenotazione/<int:pk>/", prenotazione, name="prenotazione"),
    path("situation/", my_situation, name="situation"),
    path("disdetta/<int:pk>/", disdetta, name="disdetta"),

    path("situationg/", GymSituationView.as_view(),name="situationg"),
    path("detailg/<int:pk>/", GymDetailView.as_view(), name="detailg"),
    path("crea_disciplina/",CreateDisciplinaView.as_view(),name="creadisciplina"),
    path("crea_corso/",CreateCorsoView.as_view(),name="creacorso"),
    path("elimina_disciplina/<int:pk>/",elimina_disciplina,name="eliminadisciplina"),
    path("elimina_corso/<int:pk>/",elimina_corso,name="eliminacorso"),
    path("modifica_disciplina/<int:pk>/",UpdateDisciplinaView.as_view(),name="modificadisciplina"),
    path("modifica_corso/<int:pk>/",UpdateCorsoView.as_view(),name="modificacorso"),
]                                                                       