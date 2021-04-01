from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserSerializer, TokenSerializer, EventSerializer, PropertySerializer
from .models import User, Token, Event, Property
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

AVALANCHENODE = 'http://143.198.63.78:9650/ext/bc/X'

class TokenView(generics.GenericAPIView):
    serializer_class = user_serializers.TokenSerializer
    token_model = user_models.Token
    permission_classes = (IsAuthenticatedOrReadOnly,) 
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('listed', 'listedPrice', 'owner', 'owner_id', 'property', 'property_id', 'purchasedPrice', 'tokenId')
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
        print(serializer.errors)

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
        #print(serializer.errors)

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

class UserView(generics.GenericAPIView):

    serializer_class = user_serializers.UserSerializer
    user_model = user_models.User
    permission_classes = (IsAuthenticatedOrReadOnly,) 
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ['fullName','walletAddress','user','investorTypeId','kycVerified','email']

    def get_queryset(self):
        return

    def get(self, request):
        try:
            user_obj = self.filter_queryset(self.user_model.objects.all())
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

class EventView(generics.GenericAPIView):

    serializer_class = user_serializers.EventSerializer
    event_model = user_models.Event
    token_model = user_models.Token
    user_model = user_models.User
    # permission_classes = (IsAuthenticatedOrReadOnly,) 
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('tokenOwner', 'eventCreator', 'eventDateTime', 'token', 'txNFTId', 'txAvaxId','eventType','eventId','property')
    def get_queryset(self):
        return

    def get(self, request):
        try:
            event_arr = self.filter_queryset(self.event_model.objects.all())
        except self.event_model.DoesNotExist:
            return Response('Event not found in database',
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            event_arr,
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        #Check for NFT ownership
        #Avalanche API
        #transfer NFT to receiver

        if request.data['eventType']=='SALE':
            numTokens = int(request.data['quantity'])
            tokensToBeSold = self.token_model.objects.filter(property__propertyId=int(request.data['property']),owner__realiumUserId=int(request.data['tokenOwner']),listed=True)[:numTokens]
            txNFTId = str('')
            txAvaxId = str('')
            for num in range(0,numTokens):
                token = self.token_model.objects.get(pk=tokensToBeSold[num].tokenId)
                eventCreator = self.user_model.objects.get(pk=request.data['eventCreator'])
                tokenOwner = self.user_model.objects.get(pk=request.data['tokenOwner'])

                try: 
                    array = [tokenOwner.walletAddress]
                    transferNFTResponse = requests.post(AVALANCHENODE, 
                                            json={
                                                "jsonrpc":"2.0",
                                                "id"    : 1,
                                                "method" :'avm.sendNFT',
                                                "params" :{ 
                                                    "assetID" : token.property.avalancheAssetId,
                                                    "from"    : array,
                                                    "to"      : eventCreator.walletAddress,
                                                    "groupID" : 0,
                                                    "changeAddr": eventCreator.walletAddress, #which xchain?
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
                                                "address": eventCreator.walletAddress,
                                                "assetId": "AVAX"
                                            }
                                        } 
                    
                    checkBalanceResponse = requests.post(AVALANCHENODE, 
                                json=checkBalanceJson)
                    checkBalanceResult = JSON.loads(str(checkBalanceResponse.text))
                    if int(checkBalanceResult["result"]["balance"]) < int(request.data["listedPrice"]): 
                        raise Exception("Insufficient funds")                  

                    array = [eventCreator.walletAddress]
                    transferAvaxResponse = requests.post(AVALANCHENODE, 
                                            json={
                                                    'jsonrpc':'2.0',
                                                    'id'     :1,
                                                    'method' :'avm.send',
                                                    'params' :
                                                    { 
                                                        "assetID" : 'AVAX',
                                                        "amount"  : request.data["listedPrice"],
                                                        "from"    : array,
                                                        "to"      : tokenOwner.walletAddress,
                                                        "changeAddr": tokenOwner.walletAddress,
                                                        "memo"    : "AVAX has been transferred for your sale of "+token.property.avalancheAssetId,
                                                        'username': 'capstone',
                                                        'password': 'D835$938jemv@2'
                                                    }
                                                })

                    txResponse = JSON.loads(str(transferAvaxResponse.text))

                    txAvaxId = txResponse['result']['txID']

                except:
                    #EXCEPTION THROWN FUNDS NOT SENT AND NFT RETURNED
                    array = []
                    array.append(eventCreator.walletAddress)
                    json ={
                            "jsonrpc":"2.0",
                            "id"    : 1,
                            "method" :'avm.sendNFT',
                            "params" :{ 
                                "assetID" : token.property.avalancheAssetId,
                                "from"    : array,
                                "to"      : tokenOwner.walletAddress,
                                "groupID" : 0,
                                "changeAddr": tokenOwner.walletAddress,
                                "username": "capstone",
                                "password": "D835$938jemv@2"
                            }
                        }
                    transferBackNFTResponse = requests.post(AVALANCHENODE, 
                                    json=json)
                    txResponse = JSON.loads(str(transferBackNFTResponse.text))
                    raise Exception("Insufficient funds")
                    exit

                saleEvent_dict = {
                    'token' : token.tokenId,
                    'tokenOwner' : request.data['tokenOwner'], 
                    'eventCreator' : request.data['eventCreator'],
                    'txNFTId': txNFTId,
                    'txAvaxId': txAvaxId,
                    'quantity': 1,
                    'eventType': request.data['eventType'],
                    'property': request.data['property'],
                    'listedPrice': request.data['listedPrice'], 
                    'purchasedPrice': request.data['listedPrice'],
                }

                query_dict = QueryDict('', mutable=True)
                query_dict.update(saleEvent_dict)

                #get Token
                token_obj = self.token_model.objects.get(pk=token.tokenId)
                #change Token owner
                user = self.user_model.objects.filter(walletAddress=eventCreator.walletAddress)[0]
                token_obj.owner = user
                token_obj.purchasedPrice = request.data["listedPrice"]
                #save Token
                token_obj.save()

                serializer = self.serializer_class(
                    data=query_dict
                )
                
                if serializer.is_valid():
                    serializer.save()
                print(serializer.errors)

        #if the event is not a SALE
        elif request.data['eventType']=='OFFER':
            offerEvent_dict = {
                'token' : request.data['tokenId'],
                'tokenOwner' : request.data['tokenOwner'], 
                'eventCreator' : request.data['eventCreator'],
                'txNFTId': None,
                'txAvaxId': None,
                'quantity': 1,
                'eventType': request.data['eventType'],
                'property': request.data['property'],
                'listedPrice': None, #need clarification of what offer is
                'purchasedPrice': None,
            }
            query_dict = QueryDict('', mutable=True)
            query_dict.update(offerEvent_dict)
            serializer = self.serializer_class(
                data=query_dict
            )

        elif request.data['eventType']=='LIST':
            #GET TOKEN AND CHANGE TO LISTED
            numTokens = int(request.data['quantity'])
            listedTokens = self.token_model.objects.filter(property__propertyId=int(request.data['property']),owner__realiumUserId=int(request.data['tokenOwner']),listed=False)[:numTokens]
            for num in range(0,numTokens): 
                changedToken = self.token_model.objects.get(pk=listedTokens[num].tokenId)
                changedToken.listed=True
                changedToken.listedPrice=request.data['listedPrice']
                changedToken.save()
                listedEvent_dict = {
                    'token' : listedTokens[num].tokenId,
                    'tokenOwner' : request.data['eventCreator'], 
                    'eventCreator' : request.data['eventCreator'],
                    'txNFTId': None,
                    'txAvaxId': None,
                    'quantity': 1,
                    'eventType': request.data['eventType'],
                    'property': request.data['property'],
                    'listedPrice': request.data['listedPrice'],
                    'purchasedPrice': request.data['purchasedPrice'],
                }
                query_dict = QueryDict('', mutable=True)
                query_dict.update(listedEvent_dict)
                serializer = self.serializer_class(
                    data=query_dict
                )
                if serializer.is_valid():
                    serializer.save()

        elif request.data['eventType']=='UNLIST':
            #GET TOKEN AND CHANGE TO UNLISTED
            numTokens = int(request.data['quantity'])
            unlistedTokens = self.token_model.objects.filter(property__propertyId=int(request.data['property']),owner__realiumUserId=int(request.data['tokenOwner']),listed=True)[:numTokens]
            for num in range(0,numTokens):
                changedToken = self.token_model.objects.get(pk=unlistedTokens[num].tokenId)
                changedToken.listed=False
                changedToken.save()
                listedEvent_dict = {
                    'token' : unlistedTokens[num].tokenId,
                    'tokenOwner' : request.data['eventCreator'], 
                    'eventCreator' : request.data['eventCreator'],
                    'txNFTId': None,
                    'txAvaxId': None,
                    'quantity': 1,
                    'eventType': request.data['eventType'],
                    'property': request.data['property'],
                    'listedPrice': None,
                    'purchasedPrice': None,
                }
                query_dict = QueryDict('', mutable=True)
                query_dict.update(listedEvent_dict)
                serializer = self.serializer_class(
                    data=query_dict
                )
                if serializer.is_valid():
                    serializer.save()
        else:
            exit


        if serializer:
            if serializer.is_valid():
                serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
        

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('fullName')
    serializer_class = UserSerializer

class TokenViewSet(viewsets.ModelViewSet):
    queryset = Token.objects.all().order_by('listed')
    serializer_class = TokenSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-eventDateTime')
    serializer_class = EventSerializer

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
