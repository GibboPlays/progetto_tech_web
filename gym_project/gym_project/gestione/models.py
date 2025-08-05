from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Corso(models.Model):
    nome = models.CharField(max_length=200)
    personal_trainer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="corsi_gestiti")
        
    def __str__(self):
        out = self.nome + " svolto da " + self.personal_trainer
        return out

    class Meta:
        verbose_name_plural = "Corsi"

class Occorrenza(models.Model):
    corso = models.ForeignKey(Corso, on_delete=models.CASCADE, related_name="occorrenze")
    data = models.DateField(null=True, blank=True)
    max_partecipanti = models.IntegerField()
    utenti = models.ManyToManyField(User, related_name="occorrenze_iscritto", blank=True)

    def numero_partecipanti(self):
        return self.utenti.count()

    def chi_partecipa(self):
        return ", ".join([utente.username for utente in self.utenti.all()])
    
    def disponibile(self):
        return self.num_partecipanti < self.max_partecipanti

    def __str__(self):
        return "Occorrenza di " + str(self.corso) + " ha " + self.num_partecipanti() + " partecipanti su " + self.max_partecipanti

    class Meta:
        verbose_name_plural = "Occorrenze"
