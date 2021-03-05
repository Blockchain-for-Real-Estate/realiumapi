from rest_framework import serializers

from .models import Hero, User, Asset

class HeroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hero
        fields = ('name', 'alias')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('fullName', 'investorTypeId','kycVerified','walletAddress','email')

class AssetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Asset
        fields = ('assetName', 'assetTypeId', 'opportunityType', 'legalTypeId', 'tokenId', 'parcelId', 'streetAddress',
                    'city', 'state', 'zipCode', 'country', 'acerage', 'llc')