from django import forms
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import *

class SearchForm(forms.Form):

    CHOICE_LIST = [('nome',"Cerca tra i nomi"), ('personal_trainer',"Cerca tra i personal trainers")]
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
 
    #Per avere nella choice list solo i personal trainers
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['personal_trainer'].queryset = PersonalTrainer.get_personal_trainers()

    def clean(self):

        cleaned_data = super().clean()

        nome_disciplina = cleaned_data.get('nome')
        personal_trainer = cleaned_data.get('personal_trainer')

        if not nome_disciplina:
            self.add_error('nome_disciplina',"Devi inserire il nome della disciplina")

        if not personal_trainer:
            self.add_error('personal_trainer',"Il personal trainer inserito non è valido")
        
        return cleaned_data

class CreateCorsoForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "addcorso_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Aggiungi Corso"))
    #lower bound di inserimento
    max_partecipanti = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': 1}),
        label="Numero massimo di partecipanti"
    )

    class Meta:
        model = Corso
        fields = ["disciplina","data","ora","max_partecipanti"]
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'ora': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    #Per controllare validità dei campi
    def clean(self):

        cleaned_data = super().clean()

        disciplina_corso=cleaned_data.get('disciplina')
        data_corso = cleaned_data.get('data')
        ora_corso = cleaned_data.get('ora')
        max_partecipanti = cleaned_data.get('max_partecipanti')

        if not disciplina_corso:
            self.add_error('disciplina',"La disciplina inserita non è valida")

        if data_corso and data_corso < timezone.now().date():
            self.add_error('data',"La data del corso non può essere nel passato")

        if ora_corso and data_corso and data_corso == timezone.now().date() and ora_corso < timezone.now().time():
            self.add_error('ora',"L'ora del corso non può essere nel passato")

        if max_partecipanti and max_partecipanti < 1:
            self.add_error('max_partecipanti','Il numero di partecipanti possibili deve essere almeno 1')
        
        return cleaned_data
    
class UpdateDisciplinaForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "editdisciplina_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Salva Modifiche"))

    class Meta:
        model = Disciplina
        fields = ["nome","personal_trainer"]
 
    #Per avere nella choice list solo i personal trainers
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)   
        self.fields['personal_trainer'].queryset = PersonalTrainer.get_personal_trainers()

    def clean(self):

        cleaned_data = super().clean()

        nome_disciplina = cleaned_data.get('nome')
        personal_trainer = cleaned_data.get('personal_trainer')

        if not nome_disciplina:
            self.add_error('nome',"Devi inserire il nome della disciplina")

        if not personal_trainer:
            self.add_error('personal_trainer',"Il personal trainer inserito non è valido")
        
        return cleaned_data

class UpdateCorsoForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "editcorso_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Salva Modifiche"))
    #lower bound di inserimento
    max_partecipanti = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': 1}),
        label="Numero massimo di partecipanti"
    )

    class Meta:
        model = Corso
        fields = ["disciplina","data","ora","max_partecipanti"]
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'ora': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    #Per controllare validità dei campi
    def clean(self):

        cleaned_data = super().clean()

        disciplina_corso=cleaned_data.get('disciplina')
        data_corso = cleaned_data.get('data')
        ora_corso = cleaned_data.get('ora')
        max_partecipanti = cleaned_data.get('max_partecipanti')

        if not disciplina_corso:
            self.add_error('disciplina',"La disciplina inserita non è valida")

        if data_corso and data_corso < timezone.now().date():
            self.add_error('data',"La data del corso non può essere nel passato")

        if ora_corso and data_corso and data_corso == timezone.now().date() and ora_corso < timezone.now().time():
            self.add_error('ora',"L'ora del corso non può essere nel passato")

        if max_partecipanti and max_partecipanti < 1:
            self.add_error('max_partecipanti','Il numero di partecipanti possibili deve essere almeno 1')
        
        return cleaned_data


