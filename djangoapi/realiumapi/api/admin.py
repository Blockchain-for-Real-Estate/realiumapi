from django.contrib import admin
from .models import User, Asset, Hero, Transaction

admin.site.register(User)
admin.site.register(Asset)
admin.site.register(Hero)
admin.site.register(Transaction)