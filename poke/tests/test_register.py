from poke.models import ChoicePokeModel
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls.base import reverse
from mock import patch, mock_open


class RegisterAndChoiceTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        test_user1 = User.objects.create_user(username='testuser1', password='testuser1')
        test_user1.save()
        test_user2 = User.objects.create_user(username='testuser2', password='testuser2')
        test_user2.save()

    def test_register_GET(self):
        response = self.client.get(reverse('poke:register'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poke/register.html')

    def test_register_POST(self):
        response = self.client.post(reverse('poke:register'), {
            'username' : 'player',
            'password1' : 'playerpokemon',
            'password2' : 'playerpokemon',
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(''))
        self.assertTrue(User.objects.get(username='player',))

    def test_choicepoke_notLogin_GET(self):
        response = self.client.get(reverse('poke:choicepoke'))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(''))


    def test_choicepoke_GET(self):
        self.client.login(username='testuser1', password='testuser1')
        response = self.client.get(reverse('poke:choicepoke'))

        self.assertTrue(response.context['pokes'])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poke/choicepoke.html')

        response2 = self.client.get(reverse('poke:choicepoke'), {
            'offset' : 20,
            'limit' : 20,
        })

        self.assertTrue(response2.context['pokes'])
        self.assertEqual(response2.context['next'], 'offset=40&limit=20')
        self.assertEqual(response2.context['previous'], 'offset=0&limit=20')
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'poke/choicepoke.html')


    def test_chosenpoke_notLogin_GET(self):
        response = self.client.get(reverse('poke:chosenpoke', kwargs={'name' : 'pokemon',}))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(''))

    def test_chosenpoke_notExistPokemon_GET(self):
        self.client.login(username='testuser1', password='testuser1')
        response = self.client.get(reverse('poke:chosenpoke', kwargs={'name' : 'pokemon',}))

        self.assertTrue(ChoicePokeModel.objects.count(), 1)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/pokechoice'))

        response2 = self.client.get(reverse('poke:chosenpoke', kwargs={'name' : 'pokemon',}))

        self.assertTrue(ChoicePokeModel.objects.count(), 1)
        self.assertEqual(response2.status_code, 302)
        self.assertTrue(response2.url.startswith('/pokechoice'))

