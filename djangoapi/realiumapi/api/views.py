from django.shortcuts import render
from rest_framework import viewsets
from .serializers import HeroSerializer, UserSerializer, AssetSerializer, TransactionSerializer
from .models import Hero, User, Asset, Transaction

import requests
import logging
import datetime

import django.core.exceptions as django_exceptions
import django.contrib.auth.models as auth_models
import django.db.models.functions as db_functions
import django.http as http

import rest_framework.authentication as auth
from rest_framework.permissions import IsAuthenticatedOrReadOnly
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

AVALANCHENODE = 'http://144.126.214.126/ext/bc/X'

class AssetView(APIView):

    serializer_class = user_serializers.AssetSerializer
    asset_model = user_models.Asset
    permission_classes = (IsAuthenticatedOrReadOnly,) 

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
    permission_classes = (IsAuthenticatedOrReadOnly,) 

    def get(self, request, pk):
        try:
            user_obj = self.user_model.objects.get(userId=pk)
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
    permission_classes = (IsAuthenticatedOrReadOnly,) 

    def get(self, request, pk):
        try:
            transaction_arr = self.transaction_model.objects.filter(assetId=pk)
        except self.transaction_model.DoesNotExist:
            return Response('Transaction not found in database',
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            transaction_arr,
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        #Check for NFT ownership
        transactionNFTId = str('')
        transactionAvaxId = str('')
        try:
            nftOwnershipResponse = requests.post(AVALANCHENODE, 
                                    data =
                                        {
                                            'jsonrpc':'2.0',
                                            'id'     : 1,
                                            'method' :'avm.getBalance',
                                            'params' :{
                                                'address': '{request.data.sender}',
                                                'assetID': '{request.data.assetid}'
                                            }
                                    }) 

            print("nftownershipresponse", nftOwnershipResponse)

            #THROW EXCEPTION NFT NOT FOUND
            if nftOwnershipResponse.result.balance == 0:
                x=0
        except requests.exceptions.RequestException as err:
            print ("Oops: Somebody got ya ",err)
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt) 

        try:
            #Check for Avax funds            
            avaxFundsResponse = requests.post(AVALANCHENODE, 
                                    data =
                                        {
                                            'jsonrpc':'2.0',
                                            'id'     : 1,
                                            'method' :'avm.getBalance',
                                            'params' :{
                                                'address': '{request.data.receiver}',
                                                'assetID': 'U8iRqJoiJm8xZHAacmvYyZVwqQx6uDNtQeP3CQ6fcgQk3JqnK' #AVAX assetId
                                            }
                                        }) 
            
            print("avaxFundsResponse", avaxFundsResponse)

            #THROW EXCEPTION INSUFFICIENT FUNDS
            if avaxFundsResponse.balance < request.price:
                #throw exception
                x=0
        except requests.exceptions.RequestException as err:
            print ("Oops: Somebody got ya ",err)
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt) 
            
        #Avalanche API
        #transfer NFT to receiver
        try: 
            transferNFTResponse = requests.post(AVALANCHENODE, 
                                    data =
                                        {
                                            'jsonrpc':'2.0',
                                            'id'     :1,
                                            'method' :'avm.sendNFT',
                                            'params' :{ 
                                                'assetID' : '{request.data.assetId}',
                                                'from'    : '{[request.data.sender]}',
                                                'to'      : '{request.data.receiver}',
                                                'groupID' : 0,
                                                'changeAddr': '{{xchainAddress}}', #which xchain?
                                                'username': '{request.data.sender.username}',
                                                'password': '{request.data.sender.password}' 
                                            }
                                        })
            
            print("transferNFTResponse", transferNFTResponse)

        except requests.exceptions.RequestException as err:
            print ("Oops: Somebody got ya ",err)
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt) 
            ##EXCEPTION NFT NOT TRANSFERRED
        try:
            #transfer AVAX to sender            
            transferAvaxResponse = requests.post(AVALANCHENODE, 
                                    data =
                                        {
                                            'jsonrpc':'2.0',
                                            'id'     :1,
                                            'method' :'avm.sendNFT',
                                            'params' :{ 
                                                'assetID' : 'U8iRqJoiJm8xZHAacmvYyZVwqQx6uDNtQeP3CQ6fcgQk3JqnK',
                                                'from'    : '{[request.data.receiver]}',
                                                'to'      : '{request.data.sender}',
                                                'groupID' : 0,
                                                'changeAddr': '{{xchainAddress}}', #which xchain?
                                                'username': '{request.data.receiver.username}',
                                                'password': '{request.data.receiver.password}' 
                                            }
                                        })

            print("transferAvaxResponse", transferAvaxResponse)

        except:
            #EXCEPTION THROWN FUNDS NOT SENT AND NFT RETURNED
            try:
                transferBackNFTResponse = requests.post(AVALANCHENODE, 
                                data =
                                    {
                                        'jsonrpc':'2.0',
                                        'id'     :1,
                                        'method' :'avm.sendNFT',
                                        'params' :{ 
                                            'assetID' : '{request.data.assetId}',
                                            'from'    : '{request.data.receiver}',
                                            'to'      : '{[request.data.sender]}',
                                            'groupID' : 0,
                                            'changeAddr': '{{xchainAddress}}', #which xchain?
                                            'username': '{request.data.receiver.username}',
                                            'password': '{request.data.receiver.password}' 
                                        }
                                    })
                
                print("transferBackNFTResponse", transferBackNFTResponse)
            except requests.exceptions.RequestException as err:
                print ("Oops: Somebody got ya ",err)
            except requests.exceptions.HTTPError as errh:
                print ("Http Error:",errh)
            except requests.exceptions.ConnectionError as errc:
                print ("Error Connecting:",errc)
            except requests.exceptions.Timeout as errt:
                print ("Timeout Error:",errt) 

        transaction = Transaction(request.assetId, request.price, None, request.transactionTypeId, request.sender, request.receiver,transactionNFTId, transactionAvaxId, datetime.datetime.now())

        serializer = self.serializer_class(
            data=transaction
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
    queryset = Transaction.objects.all().order_by('txDateTime')
    serializer_class = TransactionSerializer