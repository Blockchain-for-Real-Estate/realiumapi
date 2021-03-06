from django.shortcuts import render
from rest_framework import viewsets
from .serializers import HeroSerializer, UserSerializer, AssetSerializer, TransactionSerializer
from .models import Hero, User, Asset, Transaction

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
import rest_framework.decorators as api_view

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
    
    def get(self, request, pk):
        try:
            asset_obj = self.asset_model.objects.get(assetId=pk)
        except self.asset_model.DoesNotExist:
            return Response('Asset object has not been created yet',
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            asset_obj,
            many=False
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class UserView(APIView):

    serializer_class = user_serializers.UserSerializer
    user_model = user_models.User

    def get(self, request, pk):
        try:
            user_obj = user_model.objects.get(userId=pk)
        except self.user_model.DoesNotExist:
            return Response('User has not been created yet',
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            user_obj
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class TransactionView(APIView):

    serializer_class = user_serializers.TransactionSerializer
    transaction_model = user_models.Transaction

    def get(self, request, pk):
        try:
            transaction_obj = transaction_model.objects.get(transactionId=pk)
        except self.user_model.DoesNotExist:
            return Response('Transaction not found in database',
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            transaction_obj
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class HeroViewSet(viewsets.ModelViewSet):
    queryset = Hero.objects.all().order_by('name')
    serializer_class = HeroSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('fullName')
    serializer_class = UserSerializer

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all().order_by('assetName')
    serializer_class = AssetSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('transactionDateTime')
    serializer_class = TransactionSerializer