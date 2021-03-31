from rest_framework import serializers

from .models import User, Token, Transaction, Property

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = "__all__"

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

class PropertySerializer(serializers.ModelSerializer):
    tokens = TokenSerializer(many=True)

    class Meta:
        model = Property
        fields = "__all__"