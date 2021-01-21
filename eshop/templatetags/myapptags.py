from eshop.models import Setting
from django import template
from django.urls import reverse
from eCommerce import settings
from order.models import *
from product.models import *
from eshop.models import *

register = template.Library()

@register.simple_tag
def categorylist():
    return Category.objects.all()

@register.simple_tag
def shopcartcount(userid):
    count = ShopCart.objects.filter(user_id=userid).count()
    return count

@register.simple_tag
def wishlistcount(userid):
    count = WishList.objects.filter(user_id=userid).count()
    return count

@register.simple_tag
def settingslist():
    return Setting.objects.all()