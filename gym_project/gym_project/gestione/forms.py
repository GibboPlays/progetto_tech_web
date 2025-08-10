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


class CreateDisciplinaForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "adddisciplina_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Aggiungi Disciplina"))

    class Meta:
        model = Disciplina
        fields = ["nome","personal_trainer"]

class CreateCorsoForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "addcorso_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Aggiungi Corso"))

    class Meta:
        model = Corso
        fields = ["disciplina","data","max_partecipanti"]





