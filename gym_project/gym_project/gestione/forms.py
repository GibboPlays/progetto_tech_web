from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import *

class SearchForm(forms.Form):

    CHOICE_LIST = [("Nome","Cerca tra i nomi"), ("Personal Trainer","Cerca tra i personal trainers")]
    helper = FormHelper()
    helper.form_id = "search_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Cerca"))
    search_string = forms.CharField(label="Cerca qualcosa",max_length=100, min_length=3, required=True)
    search_where = forms.ChoiceField(label="Dove?", required=True, choices=CHOICE_LIST)


class CreateCorsoForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "addcorso_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Aggiungi Corso"))

    class Meta:
        model = Libro
        fields = ["nome","personal trainer"]

class CreateOccorrenzaForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "addoccorrenza_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Aggiungi Occorrenza"))

    class Meta:
        model = Occorrenza
        fields = ["corso","data","partecipanti massimi"]





