from django.db import models
from django.contrib.auth.models import User , Group, UserManager

# Create your models here.

class PersonalTrainerManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):

        user = super().create_user(username, email, password, **extra_fields)
        
        personal_trainers_group, created = Group.objects.get_or_create(name='Personal Trainers')
        user.groups.add(personal_trainers_group)
        
        return user

class AtletaManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):

        user = super().create_user(username, email, password, **extra_fields)
        
        atleti_group, created = Group.objects.get_or_create(name='Atleti')
        user.groups.add(atleti_group)
        
        return user

class PersonalTrainer(User):
    objects = PersonalTrainerManager()

    class Meta:
        proxy = True
        verbose_name = 'Personal Trainer'
        verbose_name_plural = 'Personal Trainers'
    
    @staticmethod
    def get_personal_trainers():
        try:
            group = Group.objects.get(name='Personal Trainers')
            return User.objects.filter(groups=group)
        except Group.DoesNotExist:
            return User.objects.none()
        
class Atleta(User):
    objects = AtletaManager()

    class Meta:
        proxy = True
        verbose_name = 'Atleta'
        verbose_name_plural = 'Atleti'
    
    @staticmethod
    def get_atleti():
        try:
            group = Group.objects.get(name='Atleti')
            return User.objects.filter(groups=group)
        except Group.DoesNotExist:
            return User.objects.none()

class Disciplina(models.Model):
    nome = models.CharField(max_length=200)
    personal_trainer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="discipline_gestite")
        
    def __str__(self):
        if self.personal_trainer:
            pt_nome = self.personal_trainer.username
        else:
            pt_nome = "Nessuno"
        out = self.nome + " svolto da " + pt_nome
        return out

    class Meta:
        verbose_name_plural = "Discipline"

class Corso(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name="corsi")
    data = models.DateField()
    ora = models.TimeField()
    max_partecipanti = models.IntegerField()
    utenti = models.ManyToManyField(User, related_name="corsi_iscritto", blank=True)

    def num_partecipanti(self):
        return self.utenti.count()

    def chi_partecipa(self):
        return ", ".join([utente.username for utente in self.utenti.all()])
    
    def disponibile(self):
        return self.num_partecipanti() < self.max_partecipanti

    def __str__(self):
        return "Corso di " + str(self.disciplina) + " ha " + str(self.num_partecipanti()) + " partecipanti su " + str(self.max_partecipanti)

    class Meta:
        verbose_name_plural = "Corsi"
