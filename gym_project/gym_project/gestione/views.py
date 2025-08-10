from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.http import HttpResponse

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
    #return render(request,template_name="gestione/ricerca_ajax.html",context={"form":form})

class DisciplinaRicercaView(DisciplinaListView):
    titolo = "La tua ricerca ha dato come risultato"

    def get_queryset(self):
        sstring = self.request.resolver_match.kwargs["sstring"] 
        where = self.request.resolver_match.kwargs["where"]

        if "Nome" in where:
            qq = self.model.objects.filter(nome__icontains=sstring)
        else:
            qq = self.model.objects.filter(personaltrainer__icontains=sstring)

        return qq
    
class CorsoListView(ListView):
    titolo = "Corsi riguardanti la disciplina"
    model = Corso
    template_name = "gestione/lista_corsi.html"

    def get_queryset(self):

        filtrato = Corso.objects.filter(data__gt=timezone.now().date())
        
        filtrato = filtrato.filter(disciplina__pk=self.kwargs['pk'])

        return filtrato.exclude(utenti__pk=self.request.user.pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['disciplina'] = Disciplina.objects.get(pk=self.kwargs['pk'])
        return context

def search_corso(request):

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            sstring = form.cleaned_data.get("search_string")
            where = form.cleaned_data.get("search_where")
            return redirect("gestione:ricerca_corso_risultati", sstring, where)
    else:
        form = SearchForm()

    return render(request,template_name="gestione/ricerca_corsi.html",context={"form":form})
    #return render(request,template_name="gestione/ricerca_ajax.html",context={"form":form})

class CorsoRicercaView(CorsoListView):
    titolo = "La tua ricerca ha dato come risultato"

    #Per filtrare per disciplina i corsi
    def get_queryset(self):
        sstring = self.request.resolver_match.kwargs["sstring"] 
        where = self.request.resolver_match.kwargs["where"]

        if "data" in where:
            qq = self.model.objects.filter(data__icontains=sstring)
        else:
            qq = self.model.objects.filter(max_partecipanti__icontains=sstring)

        return qq

@login_required
def prenotazione(request, pk):
    corso = get_object_or_404(Corso,pk=pk)

    errore = "NO_ERRORS"
    if corso.disponibile() == False:
        errore = "Numero di posti esauriti!"

    if corso.data < timezone.now().date():
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
    corso = get_object_or_404(Corso,pk=pk)
    user = request.user

    errore = "NO_ERRORS"
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

def get_hint(request):

    response = request.GET["q"]

    if(request.GET["w"]=="Nome"):
        q = Disciplina.objects.filter(disciplina__icontains=response)
        if len(q) > 0: 
            response = q[0].nome
    else: 
        q = Disciplina.objects.filter(personaltrainer__icontains=response)
        if len(q) > 0: 
            response = q[0].personal_trainer

    return HttpResponse(response)

#Views per soli Personal Trainers

class GymSituationView(GroupRequiredMixin, ListView):
    group_required = ["Personal Trainers"]
    model = Corso
    template_name = "gestione/situationg.html"

class GymDetailView(GroupRequiredMixin, DetailView):
    group_required = ["Personal Trainers"]
    model = Corso
    template_name = "gestione/detailg.html"

class CreateDisciplinaView(GroupRequiredMixin, CreateView):
    group_required = ["Personal Trainers"]
    title = "Aggiungi un disciplina alla palestra"
    form_class = CreateDisciplinaForm
    template_name = "gestione/create_entry.html"
    success_url = reverse_lazy("gestione:home")

class CreateCorsoView(CreateDisciplinaView):
    title = "Aggiungi una corso ad un disciplina"
    form_class = CreateCorsoForm

