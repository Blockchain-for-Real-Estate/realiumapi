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
from rest_framework import filters

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

AVALANCHENODE = 'https://ava.realium.io/ext/bc/X'

class TokenView(generics.GenericAPIView):
    serializer_class = user_serializers.TokenSerializer
    token_model = user_models.Token
    # permission_classes = (IsAuthenticatedOrReadOnly,) 
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter)
    filterset_fields = ('listed', 'listedPrice', 'owner', 'owner_id', 'property', 'property_id', 'purchasedPrice', 'tokenId')
    search_fields = ['listed', 'listedPrice', 'purchasedPrice', 'property__propertyName','property__avalancheAssetId','tokenId','owner__fullName','owner__email','owner__realiumUserId','property__city','property__zipCode','property__streetAddress','property__state','property__yearBuilt','property__country','property__acerage','property__listingType','property__propertyType']
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
    # permission_classes = (IsAuthenticatedOrReadOnly,) 
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter)
    filterset_fields = ('city','state','propertyId','propertyName','propertyTypeId','listingType','propertyType','legalTypeId','avalancheAssetId',
                        'parcelId','streetAddress','zipCode','forcastedIncome','minInvestment','maxInvestment','yearBuilt'
                        ,'country','acerage','llc')
    search_fields = ['city','state','propertyId','propertyName','propertyTypeId','listingType','propertyType','legalTypeId','avalancheAssetId',
                        'parcelId','streetAddress','zipCode','forcastedIncome','minInvestment','maxInvestment','yearBuilt'
                        ,'country','acerage','llc']
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

class UserView(generics.GenericAPIView):

    serializer_class = user_serializers.UserSerializer
    user_model = user_models.User
    # permission_classes = (IsAuthenticatedOrReadOnly,) 
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['fullName','walletAddress','user','investorTypeId','kycVerified','email']
    search_fields = ['fullName','walletAddress','investorTypeId','kycVerified','email']
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

class RegisterView(generics.GenericAPIView):
    
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


        send_avax_json = {
            "jsonrpc":"2.0",
            "id"     :1,
            "method" :"avm.send",
            "params" :{ 
                "assetID" : "AVAX",
                "amount"  : 5000000000,
                "from"    : ["X-fuji16eaqfum6a0zyltut88ps7zfn9mqffqp20nf63f"],
                "to"      : walletAddress,
                "changeAddr": "X-fuji16eaqfum6a0zyltut88ps7zfn9mqffqp20nf63f",
                "memo"    : "Initial AVAX in wallet for Realium.",
                "username": "capstone",
                "password": "D835$938jemv@2"
            }
        }

        sentInitialAvax = requests.post(AVALANCHENODE, 
                                json=send_avax_json)

        query_dict = QueryDict('', mutable=True)
        query_dict.update(user_dict)

        serializer = self.serializer_class(
            data=query_dict
        )

        if serializer.is_valid():
            serializer.save(user = newUser)

        return Response(serializer.data, status=status.HTTP_200_OK)


def resetTokenPrices(self, propertyId, tokenOwner):
    tokensCurrentlyListed = self.token_model.objects.filter(property__propertyId=int(propertyId),owner__realiumUserId=int(tokenOwner),listed=True)
    for token in tokensCurrentlyListed:
        token.listed=False
        token.price=0
        token.save()

class EventView(generics.GenericAPIView):

    serializer_class = user_serializers.EventSerializer
    event_model = user_models.Event
    token_model = user_models.Token
    property_model = user_models.Property
    user_model = user_models.User
    # permission_classes = (IsAuthenticatedOrReadOnly,) 
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter)
    filterset_fields = ('tokenOwner', 'eventCreator', 'eventDateTime', 'token','token__property__avalancheAssetId', 'txNFTId', 'txAvaxId','eventType','eventId','avalancheAssetId')
    search_fields = ['eventDateTime', 'token__property__propertyName', 'txNFTId', 'txAvaxId','eventType','eventId','avalancheAssetId']
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
        property = self.property_model.objects.get(pk=request.data["property"])
        if request.data['eventType']=='SALE':
            numTokens = int(request.data['quantity'])
            tokensToBeSold = self.token_model.objects.filter(property__propertyId=int(request.data['property']),owner__realiumUserId=int(request.data['tokenOwner']), listedPrice=float(request.data['listedPrice']),listed=True)[:numTokens]
            try:
                if numTokens!=len(tokensToBeSold):
                    raise Exception("Number of tokens does not match tokens up for sale.")
            except:
                print ("Number of tokens does not match tokens up for sale.",err)
            txNFTId = str('')
            txAvaxId = str('')
            if len(tokensToBeSold)>0:
                for num in range(0,len(tokensToBeSold)):
                    token = self.token_model.objects.get(pk=tokensToBeSold[num].tokenId)
                    eventCreator = self.user_model.objects.get(pk=int(request.data['eventCreator']))
                    tokenOwner = self.user_model.objects.get(pk=int(request.data['tokenOwner']))

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
                        if float(checkBalanceResult["result"]["balance"]) < float(request.data["listedPrice"]): 
                            raise Exception("Insufficient funds")          
                        array = [eventCreator.walletAddress]
                        transferAvaxResponse = requests.post(AVALANCHENODE+"/wallet", 
                                                json={
                                                        'jsonrpc':'2.0',
                                                        'id'     :1,
                                                        'method' :'wallet.send',
                                                        'params' :
                                                        { 
                                                            "assetID" : 'AVAX',
                                                            "amount"  : int(float(request.data["listedPrice"])*1000000000),
                                                            "from"    : array,
                                                            "to"      : tokenOwner.walletAddress,
                                                            "changeAddr": tokenOwner.walletAddress,
                                                            "memo"    : "AVAX has been transferred for your sale of "+token.property.avalancheAssetId+" for "+str(int(float(request.data["listedPrice"])*1000000000)),
                                                            'username': 'capstone',
                                                            'password': 'D835$938jemv@2'
                                                        }
                                                    })

                        txResponse = JSON.loads(str(transferAvaxResponse.text))

                        txAvaxId = txResponse['result']['txID']
                        token_obj = self.token_model.objects.get(pk=token.tokenId)
                        #change Token owner
                        user = self.user_model.objects.get(pk=eventCreator.realiumUserId)
                        token_obj.owner = user
                        token_obj.listed = False
                        token_obj.purchasedPrice = request.data["listedPrice"]
                        #save Token
                        token_obj.save()

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

                resetTokenPrices(self, request.data['property'], int(request.data['tokenOwner']))

                saleEvent_dict = {
                    'token' : None,
                    'tokenOwner' : tokenOwner.realiumUserId, 
                    'eventCreator' : eventCreator.realiumUserId,
                    'txNFTId': txNFTId,
                    'txAvaxId': txAvaxId,
                    'quantity': len(tokensToBeSold),
                    'eventType': request.data['eventType'],
                    'property': token.property.propertyId,
                    'listedPrice': request.data['listedPrice'], 
                    'purchasedPrice': request.data['listedPrice'],
                    'avalancheAssetId': token.property.avalancheAssetId
                }

                query_dict = QueryDict('', mutable=True)
                query_dict.update(saleEvent_dict)

                serializer = self.serializer_class(
                    data=query_dict
                )
                
                if serializer.is_valid():
                    serializer.save(property = property, token=token, tokenOwner=tokenOwner, eventCreator=eventCreator)

                    
                return Response(None,status=status.HTTP_200_OK)

        #if the event is not a SALE
        # elif request.data['eventType']=='OFFER':
        #     offerEvent_dict = {
        #         'token' : request.data['tokenId'],
        #         'tokenOwner' : request.data['tokenOwner'], 
        #         'eventCreator' : request.data['eventCreator'],
        #         'txNFTId': None,
        #         'txAvaxId': None,
        #         'quantity': 1,
        #         'eventType': request.data['eventType'],
        #         'property': request.data['property'],
        #         'listedPrice': None, #need clarification of what offer is
        #         'purchasedPrice': None,
        #     }
        #     query_dict = QueryDict('', mutable=True)
        #     query_dict.update(offerEvent_dict)
        #     serializer = self.serializer_class(
        #         data=query_dict
        #     )

        elif request.data['eventType']=='LIST':
            #GET TOKEN AND CHANGE TO LISTED
            numTokens = int(request.data['quantity'])
            resetTokenPrices(self, int(request.data['property']), int(request.data['tokenOwner']))
            listedTokens = self.token_model.objects.filter(property__propertyId=int(request.data['property']),owner__realiumUserId=int(request.data['tokenOwner']))[:numTokens]
            if len(listedTokens)>0:
                for num in range(0,len(listedTokens)): 
                    eventCreator = self.user_model.objects.get(pk=int(request.data['eventCreator']))
                    tokenOwner = self.user_model.objects.get(pk=int(request.data['tokenOwner']))
                    changedToken = self.token_model.objects.get(pk=listedTokens[num].tokenId)
                    changedToken.listed=True
                    changedToken.listedPrice=request.data['listedPrice']
                    changedToken.save()
                listedEvent_dict = {
                    'token' : None,
                    'tokenOwner' : request.data['eventCreator'], 
                    'eventCreator' : request.data['eventCreator'],
                    'txNFTId': None,
                    'txAvaxId': None,
                    'quantity': len(listedTokens),
                    'eventType': request.data['eventType'],
                    'property': listedTokens[num].property.propertyId,
                    'listedPrice': request.data['listedPrice'],
                    'purchasedPrice': listedTokens[num].purchasedPrice,
                }
                query_dict = QueryDict('', mutable=True)
                query_dict.update(listedEvent_dict)
                serializer = self.serializer_class(
                    data=query_dict
                )
                if serializer.is_valid():
                    serializer.save(property = property, token=changedToken, eventCreator=eventCreator, tokenOwner=tokenOwner)

                return Response(serializer.data,status=status.HTTP_200_OK)

        elif request.data['eventType']=='UNLIST':
            #GET TOKEN AND CHANGE TO UNLISTED
            resetTokenPrices(self, int(request.data['property']), int(request.data['tokenOwner']))
            numTokens = int(request.data['quantity'])
            unlistedTokens = self.token_model.objects.filter(property__propertyId=int(request.data['property']),owner__realiumUserId=int(request.data['tokenOwner']),listed=True)[:numTokens]
            if len(unlistedTokens)>0:
                for num in range(0,len(unlistedTokens)):
                    eventCreator = self.user_model.objects.get(pk=int(request.data['eventCreator']))
                    tokenOwner = self.user_model.objects.get(pk=int(request.data['tokenOwner']))
                    changedToken = self.token_model.objects.get(pk=unlistedTokens[num].tokenId)
                    changedToken.listed=False
                    changedToken.save()
                listedEvent_dict = {
                    'token' : None,
                    'tokenOwner' : request.data['eventCreator'], 
                    'eventCreator' : request.data['eventCreator'],
                    'txNFTId': None,
                    'txAvaxId': None,
                    'quantity': len(unlistedTokens),
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
                    serializer.save(property = property, token=changedToken, eventCreator=eventCreator, tokenOwner=tokenOwner)

                return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            exit
        
        return Response(None, status=status.HTTP_400_BAD_REQUEST)


        

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
