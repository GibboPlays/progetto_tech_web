from django.test import TestCase
from .models import *
from django.contrib.auth.models import User
from datetime import *
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from freezegun import freeze_time
from gym_project.asgi import application
from channels.testing import WebsocketCommunicator

class CorsoModelTest(TestCase):
    def setUp(self):
        self.atleta = Atleta.objects.create_user(username='Atleta1', password='password123')
        self.disciplina = Disciplina.objects.create(nome='Yoga')
        self.corso_pieno = Corso.objects.create(
            disciplina=self.disciplina,
            data=date(2029,11,18),
            ora=time(10,0),
            max_partecipanti=1
        )
        self.corso_disponibile = Corso.objects.create(
            disciplina=self.disciplina,
            data=date(2029,11,18),
            ora=time(11,0),
            max_partecipanti=5
        )

    def test_corso_non_disponibile_se_pieno(self):
        self.corso_pieno.utenti.add(self.atleta)
        
        self.assertFalse(self.corso_pieno.disponibile())

    def test_corso_disponibile_se_non_pieno(self):
        
        self.assertTrue(self.corso_disponibile.disponibile())

class gestione_homeTest(TestCase):
    def test_home(self):
        response = self.client.get(reverse('gestione:home'))

        self.assertEqual(response.status_code, 200)

class DisciplinaListViewTest(TestCase):
    def setUp(self):
        self.disciplina1 = Disciplina.objects.create(nome='Yoga')
        self.disciplina2 = Disciplina.objects.create(nome='Calisthenics')

    def test_lista_coerente(self):
        response = self.client.get(reverse('gestione:listadiscipline')) 
        
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['object_list']), 2)

        self.assertContains(response, 'Yoga')

        self.assertContains(response, 'Calisthenics')


class DisciplinaSearchViewTest(TestCase):
    def setUp(self):
        self.pt1 = PersonalTrainer.objects.create_user(username='PersonalTrainer1',password='password123')
        self.pt2 = PersonalTrainer.objects.create_user(username='PersonalTrainer2',password='password123')
        self.disciplina1 = Disciplina.objects.create(nome='Yoga',personal_trainer=self.pt1)
        self.disciplina2 = Disciplina.objects.create(nome='Calisthenics',personal_trainer=self.pt2)

    def test_ricerca_personal_trainer(self):

        form_data = {
            'search_string': 'PersonalTrainer1',
            'search_where': 'personal_trainer'
        }

        response = self.client.post(reverse('gestione:cercadisciplina'), form_data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.disciplina1, response.context['object_list'])
        self.assertNotIn(self.disciplina2, response.context['object_list'])

    def test_ricerca_nome(self):

        form_data = {
            'search_string': 'Calisthenics',
            'search_where': 'nome'
        }

        response = self.client.post(reverse('gestione:cercadisciplina'), form_data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.disciplina2, response.context['object_list'])
        self.assertNotIn(self.disciplina1, response.context['object_list'])

class CorsoListViewTest(TestCase):
    def setUp(self):
        self.atleta = Atleta.objects.create_user(username='Atleta1', password='password123')
        self.client.force_login(self.atleta)

        self.disciplina1 = Disciplina.objects.create(nome='Yoga')
        self.disciplina2 = Disciplina.objects.create(nome='Calisthenics')
        self.corso1 = Corso.objects.create(disciplina=self.disciplina1,data=date(2032,11,18),ora=time(10,0),max_partecipanti=23)
        self.corso2 = Corso.objects.create(disciplina=self.disciplina1,data=date(2032,11,19),ora=time(10,0),max_partecipanti=23)
        self.corso3 = Corso.objects.create(disciplina=self.disciplina2,data=date(2032,11,18),ora=time(10,0),max_partecipanti=23)

    def test_lista_disciplina(self):
        response = self.client.get(reverse('gestione:listacorsi',args=[self.disciplina1.pk])) 
        
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['object_list']), 2)

        self.assertIn(self.corso1, response.context['object_list'])
        self.assertIn(self.corso2, response.context['object_list'])
        self.assertNotIn(self.corso3, response.context['object_list'])

    #Per evitare problemi di orario in chi fa i test
    @freeze_time("2025-08-13 12:00:00")
    def test_lista_disciplina_stesso_giorno_ora_maggiore(self):
        past = timezone.now() - timedelta(hours=1)
        future = timezone.now() + timedelta(hours=1)
        
        self.corso_past = Corso.objects.create(disciplina=self.disciplina1,data=timezone.now().date(),ora=past.time(),max_partecipanti=23)
        self.corso_future = Corso.objects.create(disciplina=self.disciplina1,data=timezone.now().date(),ora=future.time(),max_partecipanti=23)

        response = self.client.get(reverse('gestione:listacorsi',args=[self.disciplina1.pk])) 
        
        self.assertEqual(response.status_code, 200)

        self.assertNotIn(self.corso_past, response.context['object_list'])
        self.assertIn(self.corso_future, response.context['object_list'])

    def test_lista_disciplina_con_prenotati(self):
        self.corso2.utenti.add(self.atleta)

        response = self.client.get(reverse('gestione:listacorsi',args=[self.disciplina1.pk])) 
        
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['object_list']), 1)

        self.assertIn(self.corso1, response.context['object_list'])
        self.assertNotIn(self.corso2, response.context['object_list'])
        self.assertNotIn(self.corso3, response.context['object_list'])

class CorsoListDailyViewTest(TestCase):
    def setUp(self):
        self.atleta = Atleta.objects.create_user(username='Atleta1', password='password123')
        self.client.force_login(self.atleta)

        self.disciplina1 = Disciplina.objects.create(nome='Yoga')
        self.disciplina2 = Disciplina.objects.create(nome='Calisthenics')
        self.corso1 = Corso.objects.create(disciplina=self.disciplina1,data=timezone.now().date(),ora=time(10,0),max_partecipanti=23)
        self.corso2 = Corso.objects.create(disciplina=self.disciplina1,data=date(2032,11,19),ora=time(10,0),max_partecipanti=23)
        self.corso3 = Corso.objects.create(disciplina=self.disciplina2,data=timezone.now().date(),ora=time(12,0),max_partecipanti=23)

    def test_lista_giornaliera(self):
        response = self.client.get(reverse('gestione:lista_corsi_giornalieri')) 
        
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['object_list']), 2)

        self.assertIn(self.corso1, response.context['object_list'])
        self.assertIn(self.corso3, response.context['object_list'])
        self.assertNotIn(self.corso2, response.context['object_list'])

    def test_lista_giornaliera_con_prenotati(self):
        self.corso3.utenti.add(self.atleta)

        response = self.client.get(reverse('gestione:lista_corsi_giornalieri')) 
        
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['object_list']), 1)

        self.assertIn(self.corso1, response.context['object_list'])
        self.assertNotIn(self.corso3, response.context['object_list'])
        self.assertNotIn(self.corso2, response.context['object_list'])


class CorsoSearchViewTest(TestCase):
    def setUp(self):
        self.atleta = Atleta.objects.create_user(username='Atleta1', password='password123')
        self.client.force_login(self.atleta)

        self.disciplina1 = Disciplina.objects.create(nome='Yoga')
        self.disciplina2 = Disciplina.objects.create(nome='Calisthenics')
        self.corso1 = Corso.objects.create(disciplina=self.disciplina1,data=date(2032,11,18),ora=time(10,0),max_partecipanti=23)
        self.corso2 = Corso.objects.create(disciplina=self.disciplina1,data=date(2032,11,19),ora=time(10,0),max_partecipanti=23)
        self.corso3 = Corso.objects.create(disciplina=self.disciplina2,data=date(2032,11,20),ora=time(12,0),max_partecipanti=23)

    def test_lista_giornaliera_cerca(self):
        data = self.corso2.data.strftime('%d-%m-%Y')
        
        response = self.client.get(
            reverse('gestione:ricerca_corso_risultati'), 
            {'ricerca': data}
        )
        
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['object_list']), 1)
        self.assertIn(self.corso2, response.context['object_list'])
        self.assertNotIn(self.corso1, response.context['object_list'])
        self.assertNotIn(self.corso3, response.context['object_list'])

    def test_lista_giornaliera_indietro(self):
        data = self.corso2.data.strftime('%d-%m-%Y')
        response = self.client.get(reverse('gestione:lista_corsi_giornalieri_data', args=[data])) 

        self.assertEqual(response.context['giorno_precedente'], self.corso1.data.strftime('%d-%m-%Y'))

        url_indietro = reverse('gestione:lista_corsi_giornalieri_data', args=[response.context['giorno_precedente']])
        response_indietro = self.client.get(url_indietro)

        self.assertEqual(response_indietro.status_code, 200)

        self.assertIn(self.corso1, response_indietro.context['object_list'])
        self.assertNotIn(self.corso2, response_indietro.context['object_list'])
        self.assertNotIn(self.corso3, response_indietro.context['object_list'])

    def test_lista_giornaliera_avanti(self):
        data = self.corso2.data.strftime('%d-%m-%Y')
        response = self.client.get(reverse('gestione:lista_corsi_giornalieri_data', args=[data])) 

        self.assertEqual(response.context['giorno_successivo'], self.corso3.data.strftime('%d-%m-%Y'))

        url_avanti = reverse('gestione:lista_corsi_giornalieri_data', args=[response.context['giorno_successivo']])
        response_avanti = self.client.get(url_avanti)

        self.assertEqual(response_avanti.status_code, 200)

        self.assertIn(self.corso3, response_avanti.context['object_list'])
        self.assertNotIn(self.corso1, response_avanti.context['object_list'])
        self.assertNotIn(self.corso2, response_avanti.context['object_list'])

class prenotazioneTest(TestCase):
    def setUp(self):
        self.atleta = Atleta.objects.create_user(username='Atleta1', password='password123')
        self.client.force_login(self.atleta)

        self.disciplina1 = Disciplina.objects.create(nome='Yoga')
        self.corso1 = Corso.objects.create(disciplina=self.disciplina1,data=date(2032,11,18),ora=time(10,0),max_partecipanti=23)
        self.corso2 = Corso.objects.create(disciplina=self.disciplina1,data=date(2032,11,19),ora=time(10,0),max_partecipanti=23)

    def test_prenotazione(self):
        self.assertNotIn(self.atleta, self.corso1.utenti.all())

        response = self.client.get(reverse('gestione:prenotazione', args=[self.corso1.pk]))

        self.assertEqual(response.status_code, 200)

        self.assertIn(self.atleta, self.corso1.utenti.all())

class my_situationTest(TestCase):
    def setUp(self):
        self.atleta = Atleta.objects.create_user(username='Atleta1', password='password123')
        self.client.force_login(self.atleta)

        self.disciplina1 = Disciplina.objects.create(nome='Yoga')
        self.corso1 = Corso.objects.create(disciplina=self.disciplina1,data=date(2032,11,18),ora=time(10,0),max_partecipanti=23)
        self.corso2 = Corso.objects.create(disciplina=self.disciplina1,data=date(2032,11,19),ora=time(10,0),max_partecipanti=23)

    def test_prenotazione(self):
        self.corso1.utenti.add(self.atleta)

        response = self.client.get(reverse('gestione:situation'))

        self.assertEqual(response.status_code, 200)

        self.assertIn(self.corso1, response.context['listacorsi'])

        self.assertNotIn(self.corso2, response.context['listacorsi'])

class disdettaTest(TestCase):
    def setUp(self):
        self.atleta = Atleta.objects.create_user(username='Atleta1', password='password123')
        self.client.force_login(self.atleta)

        self.disciplina1 = Disciplina.objects.create(nome='Yoga')
        self.corso1 = Corso.objects.create(disciplina=self.disciplina1,data=date(2032,11,18),ora=time(10,0),max_partecipanti=23)
        self.corso2 = Corso.objects.create(disciplina=self.disciplina1,data=date(2032,11,19),ora=time(10,0),max_partecipanti=23)
    
    def test_disdetta(self):
        self.corso1.utenti.add(self.atleta)
        
        self.assertIn(self.atleta, self.corso1.utenti.all())

        response = self.client.get(reverse('gestione:disdetta', args=[self.corso1.pk]))

        self.assertEqual(response.status_code, 200)

        self.assertNotIn(self.atleta, self.corso1.utenti.all())

class SearchConsumerTest(TestCase):

    def setUp(self):
        self.atleta = Atleta.objects.create_user(username='Atleta1', password='password123')
        self.client.force_login(self.atleta)
        self.personal_trainer1 = PersonalTrainer.objects.create_user(username='PersonalTrainer1', password='password123')
        self.personal_trainer2 = PersonalTrainer.objects.create_user(username='TrainerPersonal2', password='password123')   

        self.disciplina1 = Disciplina.objects.create(nome='Yoga',personal_trainer=self.personal_trainer2)
        self.disciplina2 = Disciplina.objects.create(nome='Calisthenics',personal_trainer=self.personal_trainer1)

    async def test_search_by_name(self):
        
        communicator = WebsocketCommunicator(application, "/ws/search/")

        connected, subprotocol = await communicator.connect()
        
        self.assertTrue(connected)

        await communicator.send_json_to({
            "q": "Yog",
            "w": "nome"
        })

        response = await communicator.receive_json_from()
        
        self.assertIn('response', response)
        self.assertEqual(response['response'], 'Yoga')

        await communicator.disconnect()

    async def test_search_by_trainer(self):
        communicator = WebsocketCommunicator(application, "/ws/search/")

        connected, subprotocol = await communicator.connect()
        
        self.assertTrue(connected)

        await communicator.send_json_to({
            "q": "Tra",
            "w": "personal_trainer"
        })

        response = await communicator.receive_json_from()
        
        self.assertIn('response', response)
        self.assertEqual(response['response'], 'TrainerPersonal2')

        await communicator.disconnect()
        
    async def test_no_suggestion_if_query_is_too_short(self):

        communicator = WebsocketCommunicator(application, "/ws/search/")

        connected, subprotocol = await communicator.connect()
        
        self.assertTrue(connected)

        await communicator.send_json_to({
            "q": "yo",
            "w": "nome"
        })
        
        response = await communicator.receive_json_from()
        
        self.assertIn('response', response)
        self.assertEqual(response['response'],"yo")
        
        await communicator.disconnect()

class GymSituationViewTest(TestCase):
    def setUp(self):
        self.personal_trainer = PersonalTrainer.objects.create_user(username='PersonalTrainer1', password='password123')
        self.client.login(username='PersonalTrainer1', password='password123')  

        self.disciplina1 = Disciplina.objects.create(nome='Yoga')
        self.disciplina2 = Disciplina.objects.create(nome='Calisthenics')

    def test_lista_coerente(self):
        response = self.client.get(reverse('gestione:situationg'))
        
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['object_list']), 2)

        self.assertContains(response, 'Yoga')

        self.assertContains(response, 'Calisthenics')

class GymDetailViewTest(TestCase):
    def setUp(self):
        self.personal_trainer = PersonalTrainer.objects.create_user(username='PersonalTrainer1', password='password123')
        self.client.login(username='PersonalTrainer1', password='password123')  
        
        self.disciplina1 = Disciplina.objects.create(nome='Yoga')
        self.disciplina2 = Disciplina.objects.create(nome='Calisthenics')
        self.corso1 = Corso.objects.create(disciplina=self.disciplina1,data=date(2032,11,18),ora=time(10,0),max_partecipanti=23)
        self.corso2 = Corso.objects.create(disciplina=self.disciplina1,data=date(2032,11,19),ora=time(10,0),max_partecipanti=23)
        self.corso3 = Corso.objects.create(disciplina=self.disciplina2,data=date(2032,11,20),ora=time(10,0),max_partecipanti=23)

    def test_lista_coerente(self):
        response = self.client.get(reverse('gestione:detailg', args=[self.disciplina2.pk]))
        
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['object'].corsi.all()), 1)
        self.assertIn(self.corso3, response.context['object'].corsi.all())
        self.assertNotIn(self.corso1, response.context['object'].corsi.all())
        self.assertNotIn(self.corso2, response.context['object'].corsi.all())

class CreateDisciplinaViewTest(TestCase):
    def setUp(self):
        self.personal_trainer = PersonalTrainer.objects.create_user(username='PersonalTrainer1', password='password123')
        self.client.login(username='PersonalTrainer1', password='password123')

    def test_creazione_disciplina(self):
        num = len(Disciplina.objects.all())

        dati = {
            'nome':'Yoga',
            'personal_trainer':self.personal_trainer.pk
        }
        response = self.client.post(reverse('gestione:creadisciplina'),data=dati)
        
        self.assertEqual(response.status_code, 302)

        self.assertEqual(len(Disciplina.objects.all()),num+1)

        disciplina = Disciplina.objects.get(nome='Yoga',personal_trainer__pk=self.personal_trainer.pk)

        self.assertIsNotNone(disciplina)
    
    def test_creazione_disciplina_con_get(self):
        num = len(Disciplina.objects.all())

        dati = {
            'nome':'Yoga',
            'personal_trainer':self.personal_trainer.pk
        }
        response = self.client.get(reverse('gestione:creadisciplina'),data=dati)
        
        self.assertEqual(response.status_code, 200)

        self.assertNotEqual(len(Disciplina.objects.all()),num+1)

class CreateCorsoViewTest(TestCase):
    def setUp(self):
        self.personal_trainer = PersonalTrainer.objects.create_user(username='PersonalTrainer1', password='password123')
        self.client.login(username='PersonalTrainer1', password='password123')
        
        self.disciplina1 = Disciplina.objects.create(nome='Yoga',personal_trainer=self.personal_trainer)

    def test_creazione_corso(self):
        num = len(Corso.objects.all())

        dati = {
            'disciplina':self.disciplina1.pk,
            'data':date(2032,11,18),
            'ora':time(10,0),
            'max_partecipanti':78
        }
        response = self.client.post(reverse('gestione:creacorso'),data=dati)
        
        self.assertEqual(response.status_code, 302)

        self.assertEqual(len(Corso.objects.all()),num+1)

        corso = Corso.objects.get(disciplina__pk=self.disciplina1.pk,
                                  data=date(2032,11,18),
                                  ora=time(10,0),
                                  max_partecipanti=78)
        self.assertIsNotNone(corso)
    
    def test_creazione_corso_con_get(self):
        num = len(Corso.objects.all())

        dati = {
            'disciplina':self.disciplina1.pk,
            'data':date(2032,11,18),
            'ora':time(10,0),
            'max_partecipanti':78
        }
        response = self.client.get(reverse('gestione:creacorso'),data=dati)
        
        self.assertEqual(response.status_code, 200)

        self.assertNotEqual(len(Corso.objects.all()),num+1)

class elimina_disciplinaTest(TestCase):
    def setUp(self):
        self.personal_trainer1 = PersonalTrainer.objects.create_user(username='PersonalTrainer1', password='password123')
        self.personal_trainer2 = PersonalTrainer.objects.create_user(username='PersonalTrainer2', password='password123')
        self.client.login(username='PersonalTrainer1', password='password123')  
        
        self.disciplina1 = Disciplina.objects.create(nome='Yoga',personal_trainer=self.personal_trainer1)
        self.disciplina2 = Disciplina.objects.create(nome='Calisthenics',personal_trainer=self.personal_trainer2)

    def test_elimina_disciplina_tua(self):
        response = self.client.post(reverse('gestione:eliminadisciplina',args=[self.disciplina1.pk]))
        
        self.assertEqual(response.status_code, 200)

        self.assertNotIn(self.disciplina1, Disciplina.objects.all())

    def test_elimina_disciplina_non_tua(self):
        response = self.client.post(reverse('gestione:eliminadisciplina',args=[self.disciplina2.pk]))
        
        self.assertEqual(response.status_code, 200)

        self.assertIn(self.disciplina2, Disciplina.objects.all())
    
    def test_elimina_disciplina_tua_con_get(self):
        response = self.client.get(reverse('gestione:eliminadisciplina',args=[self.disciplina1.pk]))
        
        self.assertEqual(response.status_code, 200)

        self.assertIn(self.disciplina1, Disciplina.objects.all())

class elimina_corsoTest(TestCase):
    def setUp(self):
        self.personal_trainer1 = PersonalTrainer.objects.create_user(username='PersonalTrainer1', password='password123')
        self.personal_trainer2 = PersonalTrainer.objects.create_user(username='PersonalTrainer2', password='password123')
        self.client.login(username='PersonalTrainer1', password='password123')  
        
        self.disciplina1 = Disciplina.objects.create(nome='Yoga',personal_trainer=self.personal_trainer1)
        self.disciplina2 = Disciplina.objects.create(nome='Calisthenics',personal_trainer=self.personal_trainer2)
        self.corso1 = Corso.objects.create(disciplina=self.disciplina1,data=date(2032,11,18),ora=time(10,0),max_partecipanti=23)
        self.corso2 = Corso.objects.create(disciplina=self.disciplina2,data=date(2032,11,20),ora=time(10,0),max_partecipanti=23)

    def test_elimina_corso_tuo(self):
        response = self.client.post(reverse('gestione:eliminacorso',args=[self.corso1.pk]))
        
        self.assertEqual(response.status_code, 200)

        self.assertNotIn(self.corso1, Corso.objects.all())

    def test_elimina_corso_non_tuo(self):
        response = self.client.post(reverse('gestione:eliminacorso',args=[self.corso2.pk]))
        
        self.assertEqual(response.status_code, 200)

        self.assertIn(self.corso2, Corso.objects.all())
    
    def test_elimina_corso_tuo_con_get(self):
        response = self.client.get(reverse('gestione:eliminacorso',args=[self.corso1.pk]))
        
        self.assertEqual(response.status_code, 200)

        self.assertIn(self.corso1, Corso.objects.all())

class UpdateDisciplinaViewTest(TestCase):
    def setUp(self):
        self.personal_trainer1 = PersonalTrainer.objects.create_user(username='PersonalTrainer1', password='password123')
        self.personal_trainer2 = PersonalTrainer.objects.create_user(username='PersonalTrainer2', password='password123')
        self.client.login(username='PersonalTrainer1', password='password123')  
        
        self.disciplina1 = Disciplina.objects.create(nome='Yoga',personal_trainer=self.personal_trainer1)

    def test_modifica_nome_disciplina(self):
        dati = {
            'nome':'Calisthenics',
            'personal_trainer':self.personal_trainer1.pk
        }
        response = self.client.post(reverse('gestione:modificadisciplina',args=[self.disciplina1.pk]),data=dati)
        
        self.assertEqual(response.status_code, 302)

        disciplina_aggiornata = Disciplina.objects.get(pk=self.disciplina1.pk)

        self.assertEqual(disciplina_aggiornata.nome, 'Calisthenics')

    def test_modifica_personal_trainer_disciplina(self):
        dati = {
            'nome':'Yoga',
            'personal_trainer':self.personal_trainer2.pk
        }
        response = self.client.post(reverse('gestione:modificadisciplina',args=[self.disciplina1.pk]),data=dati)
        
        self.assertEqual(response.status_code, 302)

        disciplina_aggiornata = Disciplina.objects.get(pk=self.disciplina1.pk)

        self.assertEqual(disciplina_aggiornata.personal_trainer, self.personal_trainer2)
    
    def test_modifica_nome_disciplina_con_get(self):
        dati = {
            'nome':'Calisthenics',
            'personal_trainer':self.personal_trainer1.pk
        }
        response = self.client.get(reverse('gestione:modificadisciplina',args=[self.disciplina1.pk]),data=dati)
        
        self.assertEqual(response.status_code, 200)

        disciplina_aggiornata = Disciplina.objects.get(pk=self.disciplina1.pk)

        self.assertNotEqual(disciplina_aggiornata.nome, 'Calisthenics')

class UpdateCorsoViewTest(TestCase):
    def setUp(self):
        self.personal_trainer1 = PersonalTrainer.objects.create_user(username='PersonalTrainer1', password='password123')
        self.client.login(username='PersonalTrainer1', password='password123')  
        
        self.disciplina1 = Disciplina.objects.create(nome='Yoga',personal_trainer=self.personal_trainer1)
        self.disciplina2 = Disciplina.objects.create(nome='Calisthenics',personal_trainer=self.personal_trainer1)
        self.corso1 = Corso.objects.create(disciplina=self.disciplina1,data=date(2032,11,18),ora=time(10,0),max_partecipanti=23)

    def test_modifica_disciplina_corso(self):
        dati = {
            'disciplina':self.disciplina2.pk,
            'data':date(2032,11,18),
            'ora':time(10,0),
            'max_partecipanti':23
        }
        response = self.client.post(reverse('gestione:modificacorso',args=[self.corso1.pk]),data=dati)
        
        self.assertEqual(response.status_code, 302)

        corso_aggiornato = Corso.objects.get(pk=self.corso1.pk)

        self.assertEqual(corso_aggiornato.disciplina,self.disciplina2)

    def test_modifica_data_corso(self):
        dati = {
            'disciplina':self.disciplina1.pk,
            'data':date(2032,7,19),
            'ora':time(10,0),
            'max_partecipanti':23
        }
        response = self.client.post(reverse('gestione:modificacorso',args=[self.corso1.pk]),data=dati)
        
        self.assertEqual(response.status_code, 302)

        corso_aggiornato = Corso.objects.get(pk=self.corso1.pk)

        self.assertEqual(corso_aggiornato.data,date(2032,7,19))
    
    def test_modifica_ora_corso(self):
        dati = {
            'disciplina':self.disciplina1.pk,
            'data':date(2032,11,18),
            'ora':time(18,32),
            'max_partecipanti':23
        }
        response = self.client.post(reverse('gestione:modificacorso',args=[self.corso1.pk]),data=dati)
        
        self.assertEqual(response.status_code, 302)

        corso_aggiornato = Corso.objects.get(pk=self.corso1.pk)

        self.assertEqual(corso_aggiornato.ora,time(18,32))

    def test_modifica_max_partecipanti_corso(self):
        dati = {
            'disciplina':self.disciplina1.pk,
            'data':date(2032,11,18),
            'ora':time(10,0),
            'max_partecipanti':78
        }
        response = self.client.post(reverse('gestione:modificacorso',args=[self.corso1.pk]),data=dati)
        
        self.assertEqual(response.status_code, 302)

        corso_aggiornato = Corso.objects.get(pk=self.corso1.pk)

        self.assertEqual(corso_aggiornato.max_partecipanti,78)

    def test_modifica_disciplina_corso_con_get(self):
        dati = {
            'disciplina':self.disciplina2.pk,
            'data':date(2032,11,18),
            'ora':time(10,0),
            'max_partecipanti':23
        }
        response = self.client.get(reverse('gestione:modificacorso',args=[self.corso1.pk]),data=dati)
        
        self.assertEqual(response.status_code, 200)

        corso_aggiornato = Corso.objects.get(pk=self.corso1.pk)

        self.assertNotEqual(corso_aggiornato.disciplina,self.disciplina2)




