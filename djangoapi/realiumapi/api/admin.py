from django.contrib import admin
from .models import User, Token, Event, Property

admin.site.register(User)
admin.site.register(Token)
admin.site.register(Event)
admin.site.register(Property)