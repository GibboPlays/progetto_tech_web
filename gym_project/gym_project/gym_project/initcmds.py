from gestione.models import Disciplina, Corso
from django.contrib.auth.models import User
from datetime import date

def erase_db():
    print("Cancello il DB")
    Disciplina.objects.all().delete()
    Corso.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()

def init_db():
    
    if len(Disciplina.objects.all()) != 0:
        return

    pt_names = ["Mario Rossi", "Giulia Verdi"]
    utenti_names = ["Luca Bianchi", "Chiara Neri", "Marco Gialli"]
    
    personal_trainers = []
    for nome in pt_names:
        username = nome.replace(" ", "").lower()
        user = User.objects.create_user(username=username, email=f"{username}@example.com", password="password123")
        personal_trainers.append(user)
    
    utenti = []
    for nome in utenti_names:
        username = nome.replace(" ", "").lower()
        user = User.objects.create_user(username=username, email=f"{username}@example.com", password="password123")
        utenti.append(user)

    disciplinadict = {
        "nomi" : ["Yoga", "Muay Thai", "Stretching", "Crossfit", "Calisthenics"]
    }

    for i in range(5):
        c = Disciplina()
        for k in disciplinadict:
            if k == "nomi":
                    c.nome = disciplinadict[k][i]
        c.personal_trainer = personal_trainers[i % len(personal_trainers)]
        c.save()
        for j in range(2):
            o = Corso()
            o.disciplina = c
            o.data = date(2025, 8, 10 + j)
            o.max_partecipanti = 10
            o.save()

            if j == 0:
                o.utenti.add(utenti[0], utenti[1])
            else:
                o.utenti.add(utenti[2])
    
    print("DUMP DB")
    print(Disciplina.objects.all()) #controlliamo
    print(Corso.objects.all())
