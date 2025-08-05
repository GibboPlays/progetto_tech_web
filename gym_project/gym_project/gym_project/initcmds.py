from gestione.models import Corso, Occorrenza

def erase_db():
    print("Cancello il DB")
    Corso.objects.all().delete()
    Occorrenza.objects.all().delete()

def init_db():
    
    if len(Corso.objects.all()) != 0:
        return

    corsodict = {
        "nomi" : ["Yoga", "Muay Thai", "Stretching", "Crossfit", "Calisthenics"]
    }

    for i in range(5):
        c = Corso()
        for k in corsodict:
            if k == "nomi":
                    c.nome = corsodict[k][i]
        c.save()
        for _ in range(2):
            o = Occorrenza()
            o.corso = c
            o.save()
    
    print("DUMP DB")
    print(Corso.objects.all()) #controlliamo
    print(Occorrenza.objects.all())
