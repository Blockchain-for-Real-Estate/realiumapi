from rest_framework import serializers
import django.contrib.auth.models as auth_models

from .models import User, Token, Event, Property

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
        depth = 1

class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = "__all__"
        depth = 1
        
# class TokenSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Token
#         fields = "__all__"
#         depth = 1
        
# class EventSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Event
#         fields = "__all__"
#         depth = 1
