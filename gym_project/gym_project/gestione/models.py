from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Disciplina(models.Model):
    nome = models.CharField(max_length=200)
    personal_trainer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="discipline_gestite")
        
    def __str__(self):
        pt_nome = self.personal_trainer.username if self.personal_trainer else "Nessuno"
        out = self.nome + " svolto da " + pt_nome
        return out

    class Meta:
        verbose_name_plural = "Discipline"

class Corso(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name="corsi")
    data = models.DateField(null=True, blank=True)
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
