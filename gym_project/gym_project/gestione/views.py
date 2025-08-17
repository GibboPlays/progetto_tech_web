from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.http import HttpResponse
from django.urls import reverse
import datetime
from django.utils.html import escape
from django.http import Http404

# pipenv install django-braces
from braces.views import GroupRequiredMixin

# Create your views here.

def gestione_home(request):
    return render(request,template_name="gestione/home.html")

class DisciplinaListView(ListView):
    titolo = "La nostra palestra possiede"
    model = Disciplina
    template_name = "gestione/lista_discipline.html"

def search_disciplina(request):

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            sstring = form.cleaned_data.get("search_string")
            where = form.cleaned_data.get("search_where")
            return redirect("gestione:ricerca_disciplina_risultati", sstring, where)
    else:
        form = SearchForm()

    return render(request,template_name="gestione/ricerca_discipline.html",context={"form":form})

class DisciplinaRicercaView(DisciplinaListView):
    titolo = "La tua ricerca ha dato come risultato"

    def get_queryset(self):
        sstring = self.request.resolver_match.kwargs["sstring"] 
        where = self.request.resolver_match.kwargs["where"]


        if "nome" in where:
            qq = self.model.objects.filter(nome__icontains=sstring)
        elif "personal_trainer" in where:
            qq = self.model.objects.filter(personal_trainer__username__icontains=sstring)
        else:
            qq = self.model.objects.none()

        return qq
    
class CorsoListView(ListView):
    titolo = "Corsi riguardanti la disciplina"
    model = Corso
    template_name = "gestione/lista_corsi.html"

    def get_queryset(self):

        filtrato_plus = Corso.objects.filter(data=timezone.now().date(),ora__gt=timezone.now().time())

        filtrato = Corso.objects.filter(data__gt=timezone.now().date())

        filtrato_plus = filtrato_plus.filter(disciplina__pk=self.kwargs['pk'])
        
        filtrato = filtrato.filter(disciplina__pk=self.kwargs['pk'])

        filtrato_plus = filtrato_plus.exclude(utenti__pk=self.request.user.pk)

        filtrato = filtrato.exclude(utenti__pk=self.request.user.pk)

        return filtrato.union(filtrato_plus)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['disciplina'] = get_object_or_404(Disciplina, pk=self.kwargs['pk'])
        except Http404:
            context['errore']='Disciplina non esistente'
        return context

class CorsoListDailyView(ListView):
    titolo = "Corsi del giorno"
    model = Corso
    template_name = "gestione/lista_corsi_giornalieri.html"

    def get_queryset(self):

        data_string = self.kwargs.get('data')

        #Per distinguere il caso in cui ci arrivi dal menu principale o dalle frecce
        if data_string:
            try:
                data_filtro = datetime.datetime.strptime(data_string, '%d-%m-%Y').date()
            except ValueError:
                data_filtro = timezone.now().date()
        else:
            data_filtro = timezone.now().date()

        filtrato = Corso.objects.filter(data=data_filtro)

        return filtrato.exclude(utenti__pk=self.request.user.pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        data_string = self.kwargs.get('data')

        if data_string:
            try:
                data_corrente = datetime.datetime.strptime(data_string, '%d-%m-%Y').date()
            except ValueError:
                data_corrente = timezone.now().date()
        else:
            data_corrente = timezone.now().date()

        context['data'] = data_corrente

        giorno_precedente = data_corrente - datetime.timedelta(days=1)
        giorno_successivo = data_corrente + datetime.timedelta(days=1)

        context['giorno_precedente'] = giorno_precedente.strftime('%d-%m-%Y')
        context['giorno_successivo'] = giorno_successivo.strftime('%d-%m-%Y')

        return context

class CorsoRicercaView(CorsoListDailyView):
    titolo = "La tua ricerca ha dato come risultato"

    #Per filtrare per disciplina i corsi
    def get_queryset(self):
        ricerca_query = self.request.GET.get('ricerca')

        if ricerca_query:
            try:
                data_corrente = datetime.datetime.strptime(ricerca_query, '%d-%m-%Y').date()

                qq = self.model.objects.filter(data__icontains=data_corrente)
            except ValueError:
                return Corso.objects.none()

        return qq
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ricerca_query = self.request.GET.get('ricerca')

        if ricerca_query:
            try:
                data_corrente = datetime.datetime.strptime(ricerca_query, '%d-%m-%Y').date()
            except ValueError:
                data_corrente = timezone.date()

        context['data'] = data_corrente

        giorno_precedente = data_corrente - datetime.timedelta(days=1)
        giorno_successivo = data_corrente + datetime.timedelta(days=1)

        context['giorno_precedente'] = giorno_precedente.strftime('%d-%m-%Y')
        context['giorno_successivo'] = giorno_successivo.strftime('%d-%m-%Y')

        return context
    
@login_required
def prenotazione(request, pk):
    errore = "NO_ERRORS"
    try:
        corso = get_object_or_404(Corso,pk=pk)
    except Http404:
        return render(request,"gestione/prenotazione.html",{"errore":"Corso non esistente"})

    if corso.disponibile() == False:
        errore = "Numero di posti esauriti!"

    if corso.data < timezone.now().date() or (corso.data == timezone.now().date() and corso.ora < timezone.now().time()):
        errore = "Il corso è già stato tenuto!"

    if (errore == "NO_ERRORS"):
        try:
            corso.utenti.add(request.user)
            corso.save()
            print("Prenotazione effettuata con successo " + str(corso) )
        except Exception as e:
            errore = "Errore nella prenotazione"
            print(errore + " " + str(e))

    return render(request,"gestione/prenotazione.html",{"errore":errore,"corso":corso})

@login_required
def my_situation(request):
    user = get_object_or_404(User, pk=request.user.pk)
    corsi = user.corsi_iscritto.all()
    ctx = { "listacorsi" : corsi }
    return render(request,"gestione/situation.html",ctx)

@login_required
def disdetta(request, pk):
    errore = "NO_ERRORS"
    try:
        corso = get_object_or_404(Corso,pk=pk)
    except Http404:
        return render(request,"gestione/disdetta.html",{"errore":"Corso non esistente"})
    user = request.user

    if user not in corso.utenti.all():
        errore = "Non puoi disdire una prenotazione non tua!"

    if errore == "NO_ERRORS":
        try:
            corso.utenti.remove(user)
            corso.save()
            print("Disdetta effettuata con successo " + str(corso) )
        except Exception as e:
            print("Errore! " + str(e))
            errore = "Errore nell'operazione di disdetta"

    return render(request,"gestione/disdetta.html",{"errore":errore,"corso":corso})

#Views per soli Personal Trainers

class GymSituationView(GroupRequiredMixin, ListView):
    group_required = ["Personal Trainers"]
    model = Disciplina
    template_name = "gestione/situationg.html"

class GymDetailView(GroupRequiredMixin, DetailView):
    group_required = ["Personal Trainers"]
    model = Disciplina
    template_name = "gestione/detailg.html"

class CreateDisciplinaView(GroupRequiredMixin, CreateView):
    group_required = ["Personal Trainers"]
    title = "Aggiungi una disciplina alla palestra"
    form_class = CreateDisciplinaForm
    template_name = "gestione/create_entry.html"
    success_url = reverse_lazy("gestione:home")

class CreateCorsoView(CreateDisciplinaView):
    title = "Aggiungi un corso ad una disciplina"
    form_class = CreateCorsoForm

@login_required
def elimina_disciplina(request, pk):
    errore = "NO_ERRORS"
    try:
        disciplina = get_object_or_404(Disciplina,pk=pk)
    except Http404:
        return render(request,"gestione/eliminazione_disciplina.html",{"errore":"Disciplina non esistente"})
    user = request.user

    if not user.is_staff and user != disciplina.personal_trainer:
        errore = "Non puoi eliminare una disciplina non tua!"

    #Per evitare che per sbaglio venga eliminata una disciplina
    if request.method == 'POST':
        if errore == "NO_ERRORS":
            try:
                disciplina.delete()
                print("Eliminazione effettuata con successo")
            except Exception as e:
                print("Errore! " + str(e))
                errore = "Errore nell'operazione di eliminazione"

    return render(request,"gestione/eliminazione_disciplina.html",{"errore":errore})

@login_required
def elimina_corso(request, pk):
    errore = "NO_ERRORS"
    try:
        corso = get_object_or_404(Corso,pk=pk)
    except Http404:
        return render(request,"gestione/eliminazione_corso.html",{"errore":"Corso non esistente"})
    user = request.user

    if not user.is_staff and user != corso.disciplina.personal_trainer:
        errore = "Non puoi eliminare un corso non tuo!"

    #Per evitare che per sbaglio venga eliminato un corso
    if request.method == 'POST':
        if errore == "NO_ERRORS":
            try:
                corso.delete()
                print("Eliminazione effettuata con successo")
            except Exception as e:
                print("Errore! " + str(e))
                errore = "Errore nell'operazione di eliminazione"

    return render(request,"gestione/eliminazione_corso.html",{"errore":errore})

class UpdateDisciplinaView(GroupRequiredMixin, UpdateView):
    group_required = ["Personal Trainers"]
    title = "Modifica una disciplina della palestra"
    form_class = UpdateDisciplinaForm
    model = Disciplina
    template_name = "gestione/create_entry.html"
    success_url = reverse_lazy("gestione:home")

class UpdateCorsoView(UpdateDisciplinaView):
    title = "Modifica un corso di una disciplina"
    form_class = UpdateCorsoForm
    model = Corso

