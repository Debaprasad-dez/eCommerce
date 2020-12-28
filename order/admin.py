from django.contrib import admin
from .models import *
# Register your models here.
class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['product','user', 'quantity', 'price', 'amount' ]
    list_filter = ['user']

admin.site.register(ShopCart, ShopCartAdmin)