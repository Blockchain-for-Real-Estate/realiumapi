from django.contrib import admin
from .models import User, Token, Transaction, Property

admin.site.register(User)
admin.site.register(Token)
admin.site.register(Transaction)
admin.site.register(Property)