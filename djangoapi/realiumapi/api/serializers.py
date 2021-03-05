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

        id = serializers.ReadOnlyField(required=False)
        assetName = serializers.CharField(required=True)
        assetTypeId = serializers.ReadOnlyField(required=True)
        opportunityType = serializers.CharField(
            required=True
        )
        legalTypeId = serializers.IntegerField(
            required=True
        )
        tokenId = serializers.ReadOnlyField(required=True)
        parcelId = serializers.ReadOnlyField(required=True)
        streetAddress = serializers.CharField(required=True, max_length=50)
        city = serializers.CharField(
            required=True,
            max_length=256
        )
        state = serializers.CharField(
            required=True,
            max_length=256
        )
        zip_code = serializers.IntegerField(
            required=True
        )
        country = serializers.CharField(
            required=False,
            read_only=True,
            max_length=256
        )
        acerage = serializers.FloatField(
            required=False
        )
        llc = serializers.CharField(
            required=True
        )