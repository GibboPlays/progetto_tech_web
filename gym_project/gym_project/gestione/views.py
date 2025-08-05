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


class CorsoListView(ListView):
    titolo = "La nostra palestra possiede"
    model = Corso
    template_name = "gestione/lista_corsi.html"


def search(request):

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            sstring = form.cleaned_data.get("search_string")
            where = form.cleaned_data.get("search_where")
            return redirect("gestione:ricerca_risultati", sstring, where)
    else:
        form = SearchForm()

    return render(request,template_name="gestione/ricerca.html",context={"form":form})
    #return render(request,template_name="gestione/ricerca_ajax.html",context={"form":form})

class CorsoRicercaView(CorsoListView):
    titolo = "La tua ricerca ha dato come risultato"

    def get_queryset(self):
        sstring = self.request.resolver_match.kwargs["sstring"] 
        where = self.request.resolver_match.kwargs["where"]

        if "Nome" in where:
            qq = self.model.objects.filter(nome__icontains=sstring)
        else:
            qq = self.model.objects.filter(personaltrainer__icontains=sstring)

        return qq

@login_required
def prenotazione(request, pk):
    occorrenza = get_object_or_404(Corso,pk=pk)

    errore = "NO_ERRORS"
    if occorrenza.disponibile() == False:
        errore = "Numero di posti esauriti!"

    if occorrenza.data > timezone.now():
        errore = "Il corso è già stato tenuto!"

    try:
        o.save()
        print("Prenotazione effettuata con successo " + str(occorrenza) )
    except Exception as e:
        errore = "Errore nella prenotazione"
        print(errore + " " + str(e))

    return render(request,"gestione/prestito.html",{"errore":errore,"Corso tenuto":o})

@login_required
def my_situation(request):
    user = get_object_or_404(User, pk=request.user.pk)
    occorrenze = user.occorrenze_iscritto.all()
    ctx = { "listacorsi" : occorrenze }
    return render(request,"gestione/situation.html",ctx)

class RestituisciView(LoginRequiredMixin, DetailView):
    model = Corso
    template_name = "gestione/restituzione.html"
    errore = "NO_ERRORS"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        o = ctx["object"]

        
        if self.request.user.pk in [i.pk for i in o.utenti]:
            self.errore = "Non puoi disdire una prenotazione non tua!"

        if self.errore == "NO_ERRORS":
            try:
                rem = [i for i in o.utenti if i.pk == self.request.user.pk]
                o.utenti.remove(rem[0]) = None
                o.save()
            except Exception as e:
                print("Errore! " + str(e))
                self.errore = "Errore nell'operazione di disdetta"

        return ctx

def get_hint(request):

    response = request.GET["q"]

    if(request.GET["w"]=="Nome"):
        q = Corso.objects.filter(corso__icontains=response)
        if len(q) > 0: 
            response = q[0].nome
    else: 
        q = Corso.objects.filter(personaltrainer__icontains=response)
        if len(q) > 0: 
            response = q[0].personal_trainer

    return HttpResponse(response)

#Views per soli Personal Trainers

class GymSituationView(GroupRequiredMixin, ListView):
    group_required = ["Personal Trainers"]
    model = Occorrenza
    template_name = "gestione/situationb.html"

class GymDetailView(GroupRequiredMixin, DetailView):
    group_required = ["Personal Trainers"]
    model = Occorrenza
    template_name = "gestione/detailb.html"

class CreateCorsoView(GroupRequiredMixin, CreateView):
    group_required = ["Personal Trainers"]
    title = "Aggiungi un corso alla palestra"
    form_class = CreateCorsoForm
    template_name = "gestione/create_entry.html"
    success_url = reverse_lazy("gestione:home")

class CreateOccorrenzaView(CreateCorsoView):
    title = "Aggiungi una occorrenza ad un corso"
    form_class = CreateOccorrenzaForm

