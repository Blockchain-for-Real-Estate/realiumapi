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

AVALANCHENODE = 'http://144.126.214.126/ext/bc/X'

class AssetView(generics.GenericAPIView):
    # def get(self, request):
    #     assets = Asset.objects.filter(listed=True)
    #     serializer_class = user_serializers.AssetSerializer(assets, many=True)
    #     return Response({"assets": serializer_class})
    serializer_class = user_serializers.AssetSerializer
    asset_model = user_models.Asset
    permission_classes = (IsAuthenticatedOrReadOnly,) 
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('listed','city','state','assetId','assetName','assetTypeId','listingType','propertyType','legalTypeId','tokenId',
                        'tokenNumber','parcelId','streetAddress','zipCode','originalPrice','listedPrice','forcastedIncome','minInvestment','maxInvestment','share','yearBuilt'
                        ,'country','acerage','llc','listed')

    def get(self, request):
        
        try: 
            asset_obj = self.filter_queryset(self.asset_model.objects.all())
        except self.asset_model.DoesNotExist:
            return Response('Asset object has not been created yet',
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            asset_obj,
            many=True
        )

        return Response({"assets":serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    #allow asset to be set for sale and listing price and if listed or not
    def put(self, request, pk):

        try:
            print(request.data)
            asset_obj = self.asset_model.objects.filter(assetId=pk).first()
        except self.asset_model.DoesNotExist:
            return Response('Transaction not found in database',
                            status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(
            asset_obj,
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
    filterset_fields = ['fullName','walletAddress']

    def get(self, request, pk):
        try:
            user_obj = self.user_model.objects.all()
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

class TransactionView(generics.GenericAPIView):

    serializer_class = user_serializers.TransactionSerializer
    transaction_model = user_models.Transaction
    permission_classes = (IsAuthenticatedOrReadOnly,) 
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('sender', 'receiver', 'txDateTime', 'asset', 'txNFTId', 'txAvaxId','price','txTypeId','txId')

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

    # def post(self, request):
    #     serializer = self.serializer_class(
    #         data=request.data
    #     )

    #     if serializer.is_valid():
    #         serializer.save()

    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        #Check for NFT ownership
        txNFTId = str('')
        txAvaxId = str('')
        try:
            nftOwnershipResponse = requests.post(AVALANCHENODE, 
                                    data =
                                        {
                                            'jsonrpc':'2.0',
                                            'id'     : 1,
                                            'method' :'avm.getBalance',
                                            'params' :{
                                                'address': request.data['sender'],
                                                'assetID': request.data['assetid']
                                            }
                                    }) 

            print("nftownershipresponse", nftOwnershipResponse)

            #THROW EXCEPTION NFT NOT FOUND
            if nftOwnershipResponse.result.balance == 0:
                raise requests.exceptions.RequestException("NFT is not owned.")
                exit
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
                                                'address': request.data['receiver'],
                                                'assetID': 'U8iRqJoiJm8xZHAacmvYyZVwqQx6uDNtQeP3CQ6fcgQk3JqnK' #AVAX assetId
                                            }
                                        }) 
            
            print("avaxFundsResponse", avaxFundsResponse)

            #THROW EXCEPTION INSUFFICIENT FUNDS
            if avaxFundsResponse.balance < request.data['price']:
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
                                                'assetID' : request.data['assetid'],
                                                'from'    : request.data['sender'],
                                                'to'      : request.data['receiver'],
                                                'groupID' : 0,
                                                'changeAddr': '{{xchainAddress}}', #which xchain?
                                                'username': request.data['username'],
                                                'password': request.data['password'] 
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
                                                'assetID' : 'U8iRqJoiJm8xZHAacmvYyZVwqQx6uDNtQeP3CQ6fcgQk3JqnK', #AssetId for AVAX
                                                'from'    : request.data['receiver'],
                                                'to'      : request.data['sender'],
                                                'groupID' : 0,
                                                'changeAddr': '{{xchainAddress}}', #which xchain?
                                                'username': request.data['username'],
                                                'password': request.data['password'] 
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
                                            'assetID' : request.data['assetid'],
                                            'from'    : request.data['receiver'],
                                            'to'      : request.data['sender'],
                                            'groupID' : 0,
                                            'changeAddr': '{{xchainAddress}}', #which xchain?
                                            'username': request.data['username'],
                                            'password': request.data['password'] 
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

        transaction = Transaction(None,request.data['txTypeId'],request.data['assetid'],request.data['price'], request.data['sender'], request.data['receiver'],txNFTId, txAvaxId, None)

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