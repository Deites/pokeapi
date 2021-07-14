import poke
from .forms import RegisterUserForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import ChoicePokeModel
import requests
import json
from django.views.generic.edit import ProcessFormView
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import ChoicePokeModelSerializers


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


    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        r = requests.get('https://pokeapi.co/api/v2/pokemon?offset={}&limit={}'.format(self.request.GET.get('offset'), self.request.GET.get('limit')))
        notjson = json.loads(r.content.decode('utf-8'))
        pokename = []
        for nj in notjson['results']:
            pokename.append(nj['name'])

        next = notjson['next'].split('?')[-1]
        previous = None
        if notjson['previous']: 
            previous = notjson['previous'].split('?')[-1]
        return self.render_to_response({'pokes' : pokename, 'next' : next, 'previous' : previous,})


class ChosenPoke(LoginRequiredMixin, ProcessFormView, generic.View):
    login_url = 'poke:login'

    def get(self, request, *args, **kwargs):
        exist = ChoicePokeModel.objects.filter(poke_of_user=self.request.user, pokemon=self.kwargs['name'])
        if not exist:
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

class AllPlayersList(LoginRequiredMixin, generics.ListAPIView):
    login_url = 'poke:login'
    queryset = ChoicePokeModel.objects.all()
    serializer_class = ChoicePokeModelSerializers
