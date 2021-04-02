from django.db import models
import django.contrib.auth.models as auth_models
import uuid

EVENT_TYPES = (
    ('OFFER', 'OFFER'),
    ('LIST','LIST'),
    ('SALE','SALE'),
    ('UNLIST','UNLIST')
    # ('CREATED','CREATED')
)

# Create your models here.
class User(models.Model):
    realiumUserId = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        auth_models.User,
        on_delete=models.CASCADE
    )
    fullName = models.CharField(max_length=100)
    investorTypeId = models.SmallIntegerField()
    kycVerified = models.BooleanField()
    walletAddress = models.CharField(max_length=60)
    email = models.EmailField()
    avaxusername = models.CharField(max_length=30, null=True) #currently usename and password will not be used, hard coded because of Avalanche
    avaxpassword = models.CharField(max_length=100, null=True) #set the same as their django user password, but this will be in plain text fyi
    def __str__(self):
        return self.fullName

class Property(models.Model):
    class Meta:
        ordering = ['propertyId']
    propertyId = models.AutoField(primary_key=True)
    propertyName = models.CharField(max_length=200, null=True)
    propertyTypeId = models.IntegerField(null=True, default=1)
    listingType = models.CharField(max_length=60, null=True, default="None")
    propertyType = models.CharField(max_length=60, null=True, default="None")
    legalTypeId = models.SmallIntegerField(null=True, default=1)
    avalancheAssetId = models.CharField(max_length=60, null=True) #this field will be the same for all of the tokens but I feel like we will need this for tokens, especially during transactions
    parcelId = models.CharField(max_length=60, null=True)
    streetAddress = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=60, null=True)
    state = models.CharField(max_length=60, null=True)
    zipCode = models.CharField(max_length=10, null=True)
    funded = models.IntegerField(null=True)
    forcastedIncome = models.DecimalField(max_digits= 1000, decimal_places=2, null=True)
    minInvestment = models.IntegerField(null=True)
    maxInvestment = models.IntegerField(null=True)
    yearBuilt = models.IntegerField(null=True)
    country = models.CharField(max_length=60, null=True)
    acerage = models.FloatField(max_length=60, null=True)
    llc = models.CharField(max_length=60, null=True)
    seriesCount = models.IntegerField()
    details = models.JSONField(null=True)

class Token(models.Model):
    tokenId = models.AutoField(primary_key=True)
    purchasedPrice = models.DecimalField(max_digits= 1000, decimal_places=2, null=True)
    listedPrice = models.DecimalField(max_digits= 1000, decimal_places=2,null=True)
    listed = models.BooleanField(default=False)
    property = models.ForeignKey(Property, related_name="tokens", on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User,
        verbose_name="User",
        null=True,
        on_delete=models.SET_NULL
    )
        
class Event(models.Model):
    class Meta:
        ordering = ['-eventDateTime']
    eventId = models.AutoField(primary_key=True)
    eventType = models.CharField(
                                max_length=10,
                                choices=EVENT_TYPES)
    token = models.ForeignKey(Token,verbose_name="token",null=True,on_delete=models.SET_NULL)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property')
    listedPrice = models.FloatField(null=True) #this is the amount of AVAX being sent to seller
    purchasedPrice = models.FloatField(null=True)
    tokenOwner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokenOwner') #sender of the NFT
    eventCreator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,related_name='eventCreator') #receiver of NFT
    quantity = models.IntegerField(null=True)
    txNFTId = models.CharField(max_length=200, null=True) #the transaction of sending the NFT
    txAvaxId = models.CharField(max_length=200, null=True) #the transaction of sending the AVAX
    eventDateTime = models.DateTimeField(auto_now_add=True)
    avalancheAssetId = models.CharField(max_length=60, null=True)


