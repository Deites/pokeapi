from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'poke'
urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', views.RegisterPlayer.as_view(), name='register'),
    path('pokechoice', views.PokeChoice.as_view(), name='choicepoke'),
    path('chosenpoke/<str:name>', views.ChosenPoke.as_view(), name='chosenpoke'),
    path('allplayers', views.AllPlayers.as_view(), name='allplayers'),
]