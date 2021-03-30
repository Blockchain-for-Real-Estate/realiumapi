from rest_framework import serializers

from .models import Hero, User, Asset, Transaction

class HeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hero
        fields = ('name', 'alias')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = "__all__"

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"