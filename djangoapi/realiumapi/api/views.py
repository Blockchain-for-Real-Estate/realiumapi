from django.shortcuts import render
from rest_framework import viewsets
from .serializers import HeroSerializer, UserSerializer
from .models import Hero, User


class HeroViewSet(viewsets.ModelViewSet):
    queryset = Hero.objects.all().order_by('name')
    serializer_class = HeroSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('fullName')
    serializer_class = UserSerializer
