from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .models import *
from product.models import *

# Create your views here.
def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    product_slider = Product.objects.all().order_by('-id')[:4]
    product_picked = Product.objects.all().filter(featured=True).order_by('-id')[:4]
    product_featured = Product.objects.all().order_by('?')[:4]
    page = "home"
    context = {'setting': setting, 'page': page, 'category': category, 'product_slider': product_slider, 'product_picked':product_picked, 'product_featured':product_featured }
    return render(request, 'eshop/home.html', context)

def aboutus(request):
    return HttpResponse('About Us')

def contactus(request):
    category = Category.objects.all()
    if request.method == 'POST': # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage() #create relation with model
            data.name = form.cleaned_data['name'] # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  #save data to table
            messages.success(request,"Your message has ben sent. Thank you for your message.")
            return HttpResponseRedirect('/contact')
    setting = Setting.objects.get(pk=1)
    form = ContactForm
    context={'setting':setting,'form':form, 'category': category }
    return render(request, 'eshop/contactus.html', context)

def category_products(request, id, slug):
    catdata = Category.objects.get(pk=id)
    products = Product.objects.filter(category_id=id) #default language
    context={'products': products,
             #'category':category,
             'catdata':catdata }
    return render(request, 'eshop/category_products.html',context)