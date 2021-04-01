from rest_framework import serializers

from .models import User, Token, Event, Property

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class TokenSerializer(serializers.ModelSerializer):
    property = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Token
        fields = "__all__"

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = "__all__"