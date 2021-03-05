from django.db import models
import uuid

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
    def __str__(self):
        return self.fullName

class Asset(models.Model):
    assetId = models.IntegerField(max_length=50)
    assetName = models.CharField(max_length=200)
    assetTypeId = models.IntegerField()
    opportunityType = models.CharField(max_length=60)
    legalTypeId = models.SmallIntegerField()
    tokenId = models.CharField(max_length=60)
    parcelId = models.CharField(max_length=60)
    streetAddress = models.CharField(max_length=200)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=60)
    zipCode = models.IntegerField()
    country = models.CharField(max_length=60)
    acerage = models.FloatField(max_length=60)
    llc = models.CharField(max_length=60)
    def __str__(self):
        return self.assetName