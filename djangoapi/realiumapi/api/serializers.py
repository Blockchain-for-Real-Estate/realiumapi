from rest_framework import serializers

from .models import Hero, User, Asset, Transaction

class UUIDModelSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()

class HeroSerializer(UUIDModelSerializer):
    class Meta:
        model = Hero
        fields = ('name', 'alias')

class UserSerializer(UUIDModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class AssetSerializer(UUIDModelSerializer):
    class Meta:
        model = Asset
        fields = "__all__"

class TransactionSerializer(UUIDModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"