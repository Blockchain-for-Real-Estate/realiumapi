from django.db import models
import django.contrib.auth.models as auth_models
import uuid

# Create your models here.
class User(models.Model):
    realiumUserId = models.AutoField(primary_key=True)
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
    avaxpassword = models.CharField(max_length=100, null=True) #set the same as their django user password, but this will be in plain text fyi
    def __str__(self):
        return self.fullName

class Property(models.Model):
    propertyId = models.AutoField(primary_key=True)
    propertyName = models.CharField(max_length=200, null=True)
    propertyTypeId = models.IntegerField(null=True)
    listingType = models.CharField(max_length=60, null=True)
    propertyType = models.CharField(max_length=60, null=True)
    legalTypeId = models.SmallIntegerField(null=True)
    avalancheAssetId = models.CharField(max_length=60, null=True)
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
        
class Transaction(models.Model):
    class Meta:
        ordering = ['-txDateTime']
    txId = models.AutoField(primary_key=True)
    txTypeId = models.IntegerField(null=True)
    token = models.ForeignKey(
        Token,
        verbose_name="Token",
        null=True,
        on_delete=models.SET_NULL
    )
    # property = models.ForeignKey(Property, related_name="tokens", null=True, on_delete=models.SET_NULL) #**************should this be included???????????????
    price = models.FloatField() #this is the amount of AVAX being sent to seller
    sender = models.CharField(max_length=200) #sender of the NFT
    receiver = models.CharField(max_length=200) #receiver of NFT
    txNFTId = models.CharField(max_length=200) #the transaction of sending the NFT
    txAvaxId = models.CharField(max_length=200) #the transaction of sending the AVAX
    txDateTime = models.DateTimeField(auto_now_add=True)
