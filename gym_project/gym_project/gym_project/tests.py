from django.test import TestCase
from gestione.models import *
from django.contrib.auth.models import User
from django.urls import reverse

class adminTest(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123'
        )

    def test_login_admin(self):
        get_response = self.client.get('/admin/')
        
        redirect_url = get_response.url
        self.assertIn('/admin/login/', redirect_url)    

        login_response = self.client.get(redirect_url)
        self.assertEqual(login_response.status_code, 200)
        
        #Per la sicurezza
        csrftoken = login_response.context['csrf_token']

        dati = {
            'username': 'admin',
            'password': 'password123',
            'csrfmiddlewaretoken': csrftoken,
        }

        response = self.client.post(redirect_url, data=dati, follow=True) 

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.user, self.superuser)

        self.assertTemplateUsed(response, 'admin/index.html')

class gym_homeTest(TestCase):
    def test_home(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)

class UserCreateViewTest(TestCase):
    def setUp(self):
        Group.objects.get_or_create(name='Atleti')

    def test_registrazione_atleta(self):
        num = Atleta.get_atleti().count()

        dati = {
            'username': 'Atleta1',
            'password1': ')F579JDa',
            'password2': ')F579JDa',
        }

        response = self.client.post(reverse('register'), dati)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(Atleta.get_atleti().count(), num+1)

        atleta = Atleta.objects.get(username='Atleta1')
        self.assertIsNotNone(atleta)

class loginTest(TestCase):
    def setUp(self):
        self.atleta = Atleta.objects.create_user(username='Atleta1', password='password123')
        self.personal_trainer = PersonalTrainer.objects.create_user(username='PersonalTrainer1', password='password123')
    
    def test_login_atleta(self):
        login_response = self.client.get(reverse('login'))
        self.assertEqual(login_response.status_code, 200)
        
        #Per la sicurezza
        csrftoken = login_response.context['csrf_token']

        dati = {
            'username': 'Atleta1',
            'password': 'password123',
            'csrfmiddlewaretoken': csrftoken,
        }

        response = self.client.post(reverse('login'), data=dati, follow=True) 

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.user, self.atleta)

    def test_login_personal_trainer(self):
        login_response = self.client.get(reverse('login'))
        self.assertEqual(login_response.status_code, 200)
        
        #Per la sicurezza
        csrftoken = login_response.context['csrf_token']

        dati = {
            'username': 'PersonalTrainer1',
            'password': 'password123',
            'csrfmiddlewaretoken': csrftoken,
        }

        response = self.client.post(reverse('login'), data=dati, follow=True) 

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.user, self.personal_trainer)

class logoutTest(TestCase):
    def setUp(self):
        self.atleta = Atleta.objects.create_user(username='Atleta1', password='password123')
    
    def test_logout(self):
        response = self.client.post(reverse('logout'), follow=True) 

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.wsgi_request.user, self.atleta)

class GymCreateViewTest(TestCase):
    def setUp(self):
        Group.objects.get_or_create(name='Personal Trainers')
        
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123'
        )
        self.client.force_login(self.superuser)
    
    def test_registrazione_personal_trainer(self):
        num = PersonalTrainer.get_personal_trainers().count()

        dati = {
            'username': 'PersonalTrainer1',
            'password1': ')F579JDa',
            'password2': ')F579JDa',
        }

        response = self.client.post(reverse('registerg'), dati)
        
        self.assertEqual(response.status_code, 302)

        self.assertEqual(PersonalTrainer.get_personal_trainers().count(), num+1)

        personal_trainer = PersonalTrainer.objects.get(username='PersonalTrainer1')
        self.assertIsNotNone(personal_trainer)