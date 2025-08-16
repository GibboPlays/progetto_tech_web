from gestione.models import *
from django.contrib.auth.models import User
from datetime import *
from asgiref.sync import sync_to_async

@sync_to_async
def erase_db():
    print("Cancello il DB")
    Disciplina.objects.all().delete()
    Corso.objects.all().delete()
    PersonalTrainer.objects.all().delete()
    Atleta.objects.all().delete()

@sync_to_async
def init_db():
    
    if len(Disciplina.objects.all()) != 0:
        return

    atleta1 = Atleta.objects.create_user(username='Luca Bianchi', password='password123')
    atleta2 = Atleta.objects.create_user(username='Chiara Neri', password='password123')
    atleta3 = Atleta.objects.create_user(username='Marco Gialli', password='password123')
    atleta4 = Atleta.objects.create_user(username='Alessandro Costa', password='password123')
    atleta5 = Atleta.objects.create_user(username='Davide Russo', password='password123')
    atleta6 = Atleta.objects.create_user(username='Giulia Ferrari', password='password123')
    atleta7 = Atleta.objects.create_user(username='Giovanni Ricci', password='password123')
    atleta8 = Atleta.objects.create_user(username='Luca Gallo', password='password123')
    atleta9 = Atleta.objects.create_user(username='Elisa Vitale', password='password123')
    atleta10 = Atleta.objects.create_user(username='Viola Piras', password='password123')
    atleta11 = Atleta.objects.create_user(username='Antonio Esposito', password='password123')
    atleta12 = Atleta.objects.create_user(username='Martina Conti', password='password123')
    personal_trainer1 = PersonalTrainer.objects.create_user(username='Mario Rossi', password='password123')
    personal_trainer2 = PersonalTrainer.objects.create_user(username='Giulia Verdi', password='password123')
    personal_trainer3 = PersonalTrainer.objects.create_user(username='Antonio Azzurri', password='password123')

    disciplina1 = Disciplina.objects.create(nome='Yoga',personal_trainer=personal_trainer2)
    disciplina2 = Disciplina.objects.create(nome='Muay Thai',personal_trainer=personal_trainer3)
    disciplina3 = Disciplina.objects.create(nome='Stretching',personal_trainer=personal_trainer2)
    disciplina4 = Disciplina.objects.create(nome='Crossfit',personal_trainer=personal_trainer1)
    disciplina5 = Disciplina.objects.create(nome='Calisthenics',personal_trainer=personal_trainer1)
    corso1 = Corso.objects.create(disciplina=disciplina1,data=date(2025,10,6),ora=time(10,0),max_partecipanti=50)
    corso2 = Corso.objects.create(disciplina=disciplina1,data=date(2025,11,6),ora=time(10,0),max_partecipanti=50)
    corso3 = Corso.objects.create(disciplina=disciplina1,data=date(2025,12,6),ora=time(10,0),max_partecipanti=50)
    corso4 = Corso.objects.create(disciplina=disciplina2,data=date(2025,10,7),ora=time(11,0),max_partecipanti=50)
    corso5 = Corso.objects.create(disciplina=disciplina2,data=date(2025,11,7),ora=time(11,0),max_partecipanti=50)
    corso6 = Corso.objects.create(disciplina=disciplina2,data=date(2025,12,7),ora=time(11,0),max_partecipanti=50)
    corso7 = Corso.objects.create(disciplina=disciplina3,data=date(2025,10,8),ora=time(14,0),max_partecipanti=50)
    corso8 = Corso.objects.create(disciplina=disciplina3,data=date(2025,11,8),ora=time(14,0),max_partecipanti=50)
    corso9 = Corso.objects.create(disciplina=disciplina3,data=date(2025,12,8),ora=time(14,0),max_partecipanti=50)
    corso10 = Corso.objects.create(disciplina=disciplina4,data=date(2025,10,9),ora=time(10,0),max_partecipanti=50)
    corso11 = Corso.objects.create(disciplina=disciplina4,data=date(2025,11,9),ora=time(10,0),max_partecipanti=50)
    corso12 = Corso.objects.create(disciplina=disciplina4,data=date(2025,12,9),ora=time(10,0),max_partecipanti=50)
    corso13 = Corso.objects.create(disciplina=disciplina5,data=date(2025,10,10),ora=time(16,0),max_partecipanti=50)
    corso14 = Corso.objects.create(disciplina=disciplina5,data=date(2025,11,10),ora=time(16,0),max_partecipanti=50)
    corso15 = Corso.objects.create(disciplina=disciplina5,data=date(2025,12,10),ora=time(16,0),max_partecipanti=50)

    corso7.utenti.add(atleta1)
    corso2.utenti.add(atleta2)
    corso4.utenti.add(atleta3)
    corso10.utenti.add(atleta4)
    corso13.utenti.add(atleta5)
    corso1.utenti.add(atleta6)
    corso8.utenti.add(atleta7)
    corso5.utenti.add(atleta8)
    corso11.utenti.add(atleta9)
    corso14.utenti.add(atleta10)
    corso9.utenti.add(atleta11)
    corso3.utenti.add(atleta12)
    
    print("DUMP DB")
    print(Disciplina.objects.all()) #controlliamo
    print(Corso.objects.all())
