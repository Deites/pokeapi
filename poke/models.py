from django.db import models
from django.contrib.auth.models import User

class ChoicePokeModel(models.Model):
    poke_of_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pokeofuser')
    
    pokemon = models.CharField(verbose_name='Pokemon', max_length=100, default='')

    def __str__(self):
        return self.pokemon
