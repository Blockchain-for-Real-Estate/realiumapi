from django.db import models
import uuid
from utils import create_new_ref_number

# Create your models here.
class Hero(models.Model):
    name = models.CharField(max_length=60)
    alias = models.CharField(max_length=60)
    def __str__(self):
        return self.name

class User(models.Model):
    userId = models.IntegerField()
    fullName = models.CharField(max_length=100)
    investorTypeId = models.SmallIntegerField()
    kycVerified = models.BooleanField()
    walletAddress = models.CharField(max_length=30)
    email = models.EmailField()
    avaxusername = models.CharField(max_length=30)
    avaxpassword = models.CharField(max_length=100)
    def __str__(self):
        return self.fullName

class Asset(models.Model):
    assetId = models.CharField(max_length=200, null=True)
    assetName = models.CharField(max_length=200, null=True)
    assetTypeId = models.IntegerField(null=True)
    listingType = models.CharField(max_length=60, null=True)
    propertyType = models.CharField(max_length=60, null=True)
    legalTypeId = models.SmallIntegerField(null=True)
    tokenId = models.CharField(max_length=60, null=True)
    parcelId = models.CharField(max_length=60, null=True)
    streetAddress = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=60, null=True)
    state = models.CharField(max_length=60, null=True)
    zipCode = models.CharField(max_length=10, null=True)
    price = models.IntegerField(null=True)
    funded = models.IntegerField(null=True)
    forcastedIncome = models.IntegerField(null=True)
    minInvestment = models.IntegerField(null=True)
    maxInvestment = models.IntegerField(null=True)
    share = models.IntegerField(null=True)
    yearBuilt = models.IntegerField(null=True)
    country = models.CharField(max_length=60, null=True)
    acerage = models.FloatField(max_length=60, null=True)
    llc = models.CharField(max_length=60, null=True)
    def __str__(self):
        return self.assetName

class Transaction(models.Model):
    class Meta:
        ordering = ['-transactionDateTime']
    txId = models.CharField(
        max_length = 20,
        editable=False,
        null=False,            
        unique=True,
        default=create_new_ref_number()) #create_new_ref_number
    txTypeId = models.IntegerField()
    assetId = models.ForeignKey(
        Asset,
        verbose_name="Asset",
        null=True,
        on_delete=models.SET_NULL
    )
    price = models.IntegerField() #this is the amount of AVAX being sent to seller
    sender = models.CharField(max_length=200) #sender of the NFT
    receiver = models.CharField(max_length=200) #receiver of NFT
    txNFTId = models.CharField(max_length=200) #the transaction of sending the NFT
    txAvaxId = models.CharField(max_length=200) #the transaction of sending the AVAX
    txDateTime = models.DateTimeField(auto_now_add=True)