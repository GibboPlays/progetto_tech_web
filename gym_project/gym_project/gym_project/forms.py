from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

class CreaUtenteAtleta(UserCreationForm):

    def save(self, commit=True):
        user = super().save(commit)
        g = Group.objects.get(name="Atleti")
        g.user_set.add(user)
        return user 

class CreaUtentePersonalTrainer(UserCreationForm):
    
    def save(self, commit=True):
        user = super().save(commit) 
        g = Group.objects.get(name="Personal Trainers") 
        g.user_set.add(user) 
        return user 
