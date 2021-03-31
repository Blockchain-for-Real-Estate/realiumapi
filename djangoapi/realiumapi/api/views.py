from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserSerializer, TokenSerializer, TransactionSerializer, PropertySerializer
from .models import User, Token, Transaction, Property
from django.contrib.auth.models import User as AuthUser

import requests
import logging
import datetime
import json as JSON

import django.core.exceptions as django_exceptions
import django.contrib.auth.models as auth_models
import django.db.models.functions as db_functions
import django.http as http
from django.http import QueryDict

import django_filters.rest_framework

import rest_framework.authentication as auth
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import rest_framework.status as status
import rest_framework.response as response
import rest_framework.reverse as reverse
import rest_framework.views as views
from rest_framework import generics

import realiumapi.settings as settings
import api.models as user_models
import api.serializers as user_serializers

# Aliases
APIView = views.APIView
Response = response.Response
SessionAuth = auth.SessionAuthentication

AVALANCHENODE = 'http://128.199.5.6:9650/ext/bc/X'

class TokenView(generics.GenericAPIView):
    serializer_class = user_serializers.TokenSerializer
    token_model = user_models.Token
    permission_classes = (IsAuthenticatedOrReadOnly,) 
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('listed', 'listedPrice', 'owner', 'owner_id', 'property', 'property_id', 'purchasedPrice', 'tokenId', 'transaction')
    def get_queryset(self):
        return

    def get(self, request):
        
        try: 
            token_obj = self.filter_queryset(self.token_model.objects.all())
        except self.token_model.DoesNotExist:
            return Response('Token object has not been created yet',
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            token_obj,
            many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    #allow Token to be set for sale and listing price and if listed or not
    def put(self, request, pk):

        try:
            token_obj = self.token_model.objects.filter(tokenId=pk).first()
        except self.token_model.DoesNotExist:
            return Response('Token not found in database',
                            status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(
            token_obj,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class PropertyView(generics.GenericAPIView):
    serializer_class = user_serializers.PropertySerializer
    token_model = user_models.Property
    permission_classes = (IsAuthenticatedOrReadOnly,) 
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('city','state','propertyId','propertyName','propertyTypeId','listingType','propertyType','legalTypeId','avalancheAssetId',
                        'parcelId','streetAddress','zipCode','forcastedIncome','minInvestment','maxInvestment','yearBuilt'
                        ,'country','acerage','llc')
    def get_queryset(self):
        return

    def get(self, request):
        
        try: 
            token_obj = self.filter_queryset(self.token_model.objects.all())
        except self.token_model.DoesNotExist:
            return Response('Property object has not been created yet',
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            token_obj,
            many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    #allow Token to be set for sale and listing price and if listed or not
    def put(self, request, pk):

        try:
            token_obj = self.token_model.objects.filter(tokenId=pk).first()
        except self.token_model.DoesNotExist:
            return Response('Property not found in database',
                            status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(
            token_obj,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class UserView(APIView):

    serializer_class = user_serializers.UserSerializer
    user_model = user_models.User
    permission_classes = (IsAuthenticatedOrReadOnly,) 
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['fullName','walletAddress','user','investorTypeId','kycVerified','email']

    def get(self, request):
        try:
            user_obj = self.user_model.objects.all()
        except self.user_model.DoesNotExist:
            return Response('User has not been created yet',
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            user_obj,
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

class RegisterView(APIView):
    
    serializer_class = user_serializers.UserSerializer
    user_model = user_models.User

    def post(self, request):

        newUser = AuthUser.objects.create_user(request.data['email'], request.data['email'], request.data['avaxpassword'])

        json = {
            "jsonrpc": "2.0",
            "method": "avm.createAddress",
            "params": {
                "username":"capstone",
                "password":"D835$938jemv@2" 
            },
            "id": 1
        }

        createWalletAddress = requests.post(AVALANCHENODE, 
                            json=json)

        walletResponse = JSON.loads(str(createWalletAddress.text))
        walletAddress = walletResponse['result']['address']

        user_dict = {
            'user': newUser.id,
            'fullName' : request.data['fullName'],
            'investorTypeId' : request.data['investorTypeId'],
            'kycVerified': request.data['kycVerified'], 
            'walletAddress' : walletAddress, 
            'email' : request.data['email'],
            'avaxusername': request.data['avaxusername'],
            'avaxpassword':request.data['avaxpassword'],
        }

        query_dict = QueryDict('', mutable=True)
        query_dict.update(user_dict)

        serializer = self.serializer_class(
            data=query_dict
        )

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class TransactionView(generics.GenericAPIView):

    serializer_class = user_serializers.TransactionSerializer
    transaction_model = user_models.Transaction
    token_model = user_models.Token
    user_model = user_models.User
    permission_classes = (IsAuthenticatedOrReadOnly,) 
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('sender', 'receiver', 'txDateTime', 'Token', 'txNFTId', 'txAvaxId','price','txTypeId','txId')

    def get(self, request):
        try:
            transaction_arr = self.filter_queryset(self.transaction_model.objects.all())
        except self.transaction_model.DoesNotExist:
            return Response('Transaction not found in database',
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            transaction_arr,
            many=True
        )
        return Response({"transactions":serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        #Check for NFT ownership
        txNFTId = str('')
        txAvaxId = str('')
        Token = self.token_model.objects.get(pk=request.data['tokenId'])
        #Avalanche API
        #transfer NFT to receiver
        try: 
            array = [request.data['sender']]
            transferNFTResponse = requests.post(AVALANCHENODE, 
                                    json={
                                        "jsonrpc":"2.0",
                                        "id"    : 1,
                                        "method" :'avm.sendNFT',
                                        "params" :{ 
                                            "tokenID" : Token.avalancheAssetId,
                                            "from"    : array,
                                            "to"      : request.data['receiver'],
                                            "groupID" : 0,
                                            "changeAddr": request.data['receiver'], #which xchain?
                                            "username": "capstone",
                                            "password": "D835$938jemv@2"
                                        }
                                    })
            

            txResponse = JSON.loads(str(transferNFTResponse.text))

            if 'error' in txResponse:
                if 'insufficient funds' in txResponse['error']['message']:
                    raise Exception("NFT not owned, please select an Token available to sell")
                raise Exception(txResponse['error']['message'])
            else:
                txNFTId = txResponse['result']['txID']

        except requests.exceptions.RequestException as err:
            print ("Oops: Somebody got ya ",err)
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt) 

        #Transfer AVAX to sender
        try:
            checkBalanceJson ={
                                    "jsonrpc":"2.0",
                                    "id"     : 1,
                                    "method" :"avm.getBalance",
                                    "params" :{
                                        "address": request.data['receiver'],
                                        "tokenID": "AVAX"
                                    }
                                } 
            
            checkBalanceResponse = requests.post(AVALANCHENODE, 
                        json=checkBalanceJson)
            checkBalanceResult = JSON.loads(str(checkBalanceResponse.text))
            if int(checkBalanceResult["result"]["balance"]) < int(request.data["price"]): 
                raise Exception("Insufficient funds")                  

            array = [request.data['receiver']]
            transferAvaxResponse = requests.post(AVALANCHENODE, 
                                    json={
                                            'jsonrpc':'2.0',
                                            'id'     :1,
                                            'method' :'avm.send',
                                            'params' :
                                            { 
                                                "tokenID" : 'AVAX',
                                                "amount"  : request.data["price"],
                                                "from"    : array,
                                                "to"      : request.data['sender'],
                                                "changeAddr": request.data['sender'],
                                                "memo"    : "AVAX has been transferred for your sale of "+Token.avalancheAssetId,
                                                'username': 'capstone',
                                                'password': 'D835$938jemv@2'
                                            }
                                        })

            txResponse = JSON.loads(str(transferAvaxResponse.text))

            txAvaxId = txResponse['result']['txID']

        except:
            #EXCEPTION THROWN FUNDS NOT SENT AND NFT RETURNED
            array = []
            array.append(request.data['receiver'])
            json ={
                    "jsonrpc":"2.0",
                    "id"    : 1,
                    "method" :'avm.sendNFT',
                    "params" :{ 
                        "tokenID" : Token.avalancheAssetId,
                        "from"    : array,
                        "to"      : request.data['sender'],
                        "groupID" : 0,
                        "changeAddr": request.data['sender'],
                        "username": "capstone",
                        "password": "D835$938jemv@2"
                    }
                }
            transferBackNFTResponse = requests.post(AVALANCHENODE, 
                            json=json)
            txResponse = JSON.loads(str(transferBackNFTResponse.text))
            raise Exception("Insufficient funds")
            exit

        transction_dict = {
            'txTypeId' : request.data['txTypeId'],
            'Token' : request.data['tokenId'],
            'price': request.data['price'], 
            'sender' : request.data['sender'], 
            'receiver' : request.data['receiver'],
            'txNFTId': txNFTId,
            'txAvaxId':txAvaxId
        }
        query_dict = QueryDict('', mutable=True)
        query_dict.update(transction_dict)

        #get Token
        token_obj = self.token_model.objects.get(pk=request.data['tokenId'])
        #change Token owner
        user = self.user_model.objects.filter(walletAddress=request.data['receiver'])[0]
        token_obj.owner = user
        token_obj.purchasedPrice = request.data["price"]
        #save Token
        token_obj.save()

        serializer = self.serializer_class(
            data=query_dict
        )

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('fullName')
    serializer_class = UserSerializer

class TokenViewSet(viewsets.ModelViewSet):
    queryset = Token.objects.all().order_by('listed')
    serializer_class = TokenSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('txDateTime')
    serializer_class = TransactionSerializer

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
