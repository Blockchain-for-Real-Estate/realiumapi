from django.shortcuts import render
from rest_framework import viewsets
from .serializers import HeroSerializer, UserSerializer
from .models import Hero, User

import logging

import django.core.exceptions as django_exceptions
import django.contrib.auth.models as auth_models
import django.db.models.functions as db_functions
import django.http as http

import rest_framework.authentication as auth
import rest_framework.permissions as permissions
import rest_framework.status as status
import rest_framework.response as response
import rest_framework.reverse as reverse
import rest_framework.views as views

import realiumapi.settings as settings
import api.models as user_models
import api.serializers as user_serializers

# Aliases
APIView = views.APIView
Response = response.Response
SessionAuth = auth.SessionAuthentication

class AssetView(APIView):
    serializer_class = user_serializers.AssetSerializer
    asset_model = user_models.Asset
    user_model = user_models.User

    def get(self, request):
        try:
            asset_obj = self.asset_model.objects.get(assetId=request.assetId)
        except self.asset_model.DoesNotExist:
            return Response('Asset object has not been created yet',
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            asset_obj
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

class HeroViewSet(viewsets.ModelViewSet):
    queryset = Hero.objects.all().order_by('name')
    serializer_class = HeroSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('fullName')
    serializer_class = UserSerializer
