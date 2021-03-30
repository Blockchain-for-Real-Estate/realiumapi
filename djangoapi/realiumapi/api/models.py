from django.db import models
import django.contrib.auth.models as auth_models
import uuid

# Create your models here.
class Hero(models.Model):
    name = models.CharField(max_length=60)
    alias = models.CharField(max_length=60)
    def __str__(self):
        return self.name

class User(models.Model):
    realiumUserId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, format='hex_verbose')
    user = models.OneToOneField(
        auth_models.User,
        on_delete=models.CASCADE,
        related_name='user'
    )
    fullName = models.CharField(max_length=100)
    investorTypeId = models.SmallIntegerField()
    kycVerified = models.BooleanField()
    walletAddress = models.CharField(max_length=60)
    email = models.EmailField()
    avaxusername = models.CharField(max_length=30, null=True) #currently usename and password will not be used, hard coded because of Avalanche
    avaxpassword = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.fullName

class Asset(models.Model):
    assetId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, format='hex_verbose')
    assetName = models.CharField(max_length=200, null=True)
    assetTypeId = models.IntegerField(null=True)
    listingType = models.CharField(max_length=60, null=True)
    propertyType = models.CharField(max_length=60, null=True)
    legalTypeId = models.SmallIntegerField(null=True)
    avalancheAssetId = models.CharField(max_length=60, null=True)
    tokenNumber = models.CharField(max_length=60, null=True)
    parcelId = models.CharField(max_length=60, null=True)
    streetAddress = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=60, null=True)
    state = models.CharField(max_length=60, null=True)
    zipCode = models.CharField(max_length=10, null=True)
    purchasedPrice = models.DecimalField(max_digits= 1000, decimal_places=2, null=True)
    listedPrice = models.DecimalField(max_digits= 1000, decimal_places=2,null=True)
    funded = models.IntegerField(null=True)
    forcastedIncome = models.DecimalField(max_digits= 1000, decimal_places=2, null=True)
    minInvestment = models.IntegerField(null=True)
    maxInvestment = models.IntegerField(null=True)
    share = models.IntegerField(null=True)
    yearBuilt = models.IntegerField(null=True)
    country = models.CharField(max_length=60, null=True)
    acerage = models.FloatField(max_length=60, null=True)
    llc = models.CharField(max_length=60, null=True)
    details = models.JSONField(null=True)
    #Sq ft, bedrooms, bathrooms, 
    listed = models.BooleanField(default=False)
    owner = models.ForeignKey(
        User,
        verbose_name="User",
        null=True,
        on_delete=models.SET_NULL
    )
    def __str__(self):
        return self.assetName
        
class Transaction(models.Model):
    class Meta:
        ordering = ['-txDateTime']
    txId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, format='hex_verbose')
    txTypeId = models.IntegerField(null=True)
    asset = models.ForeignKey(
        Asset,
        verbose_name="Asset",
        null=True,
        on_delete=models.SET_NULL
    )
    price = models.FloatField() #this is the amount of AVAX being sent to seller
    sender = models.CharField(max_length=200) #sender of the NFT
    receiver = models.CharField(max_length=200) #receiver of NFT
    txNFTId = models.CharField(max_length=200) #the transaction of sending the NFT
    txAvaxId = models.CharField(max_length=200) #the transaction of sending the AVAX
    txDateTime = models.DateTimeField(auto_now_add=True)