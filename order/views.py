from product.models import *
from order.models import *
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.contrib import messages

# Create your views here.
def index(request):
    return HttpResponse("Hello Order")

def addtoshopcart(request,id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    product= Product.objects.get(pk=id)
    checkinproduct = ShopCart.objects.filter(product_id=id) # Check product in shopcart
    if checkinproduct:
        control = 1 # The product is in the cart
    else:
        control = 0 # The product is not in the cart"""

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control==1: # Update  shopcart
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()  # save data
            else : # Inser to Shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id =id
                # data.variant_id = variantid
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Product added to Shopcart ")
        return HttpResponseRedirect(url)

    else: # if there is no post
        if control == 1:  # Update  shopcart
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1
            data.save()  #
        else:  #  Inser to Shopcart
            data = ShopCart()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            # data.variant_id =None
            data.save()  #
        messages.success(request, "Product added to Shopcart")
        return HttpResponseRedirect(url)
