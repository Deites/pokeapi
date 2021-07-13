from .forms import RegisterUserForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import ChoicePokeModel
import requests
import json
from django.views.generic.edit import ProcessFormView
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.models import User


class Login(generic.TemplateView):
    template_name = 'poke/index.html'

class RegisterPlayer(generic.CreateView):
    template_name = 'poke/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('poke:login')

class PokeChoice(LoginRequiredMixin, generic.ListView):
    login_url = 'poke:login'
    model = ChoicePokeModel
    template_name = 'poke/choicepoke.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        r = requests.get('https://pokeapi.co/api/v2/pokemon')
        notjson = json.loads(r.content.decode('utf-8'))
        pokename = []
        for nj in notjson['results']:
            pokename.append(nj['name'])
        context['pokes'] = pokename
        return context

class ChosenPoke(LoginRequiredMixin, ProcessFormView, generic.View):
    login_url = 'poke:login'

    def get(self, request, *args, **kwargs):
        ChoicePokeModel.objects.create(poke_of_user=self.request.user, pokemon=self.kwargs['name'])
        return HttpResponseRedirect(reverse_lazy('poke:choicepoke'))

class AllPlayers(LoginRequiredMixin, generic.ListView):
    login_url = 'poke:login'
    model = ChoicePokeModel
    template_name = 'poke/allplayers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        allusers = User.objects.all()
        usersDict = {}
        for a in allusers:
            pokemons = []
            for poke in a.pokeofuser.all():
                pokemons.append(poke.pokemon)
            usersDict[a.username] = ', '.join(pokemons)
        context['usersDict'] = usersDict
        return context