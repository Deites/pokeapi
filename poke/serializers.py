from django.contrib.auth import models
from django.db.models import fields
from rest_framework import serializers
from .models import ChoicePokeModel

class ChoicePokeModelSerializers(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='poke_of_user.username')
    
    class Meta:
        model = ChoicePokeModel
        fields = ('owner', 'pokemon')