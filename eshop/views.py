from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib import messages
import json
from .models import *
from product.models import *
from .forms import *

# Create your views here.
page = 1

def index(request):
    global page
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    # men = Category.objects.get(title = 'Men')
    # child = men.get_children()
    product_slider = Product.objects.all().order_by('-id')[:10]
    product_picked = Product.objects.all().filter(
        featured=True).order_by('-id')[:4]
    product_trending = Product.objects.all().order_by('?')[:12]
    page = page-1
    print(request.user.username)
    context = {'setting': setting, 'page': page, 'category': category, 'product_slider': product_slider, 'range': range(
        1, len(product_slider)), 'product_picked': product_picked, 'product_trending': product_trending, # 'men': men, 'child': child
               }
    return render(request, 'eshop/home.html', context)


def aboutus(request):
    return HttpResponse('About Us')


def contactus(request):
    category = Category.objects.all()
    if request.method == 'POST':  # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()  # create relation with model
            data.name = form.cleaned_data['name']  # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # save data to table
            messages.success(
                request, "Your message has ben sent. Thank you for your message.")
            return HttpResponseRedirect('/contact')
    setting = Setting.objects.get(pk=1)
    form = ContactForm
    context = {'setting': setting, 'form': form, 'category': category}
    return render(request, 'eshop/contactus.html', context)


def category_products(request, id, slug):
    catdata = Category.objects.get(pk=id)
    products = Product.objects.filter(category_id=id)  # default language
    context = {'products': products,
               # 'category':category,
               'catdata': catdata}
    return render(request, 'eshop/category_products.html', context)


def search(request):
    if request.method == 'POST':  # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']  # get form input data
            if len(query) > 300:
                products = Product.objects.none()
            else:
                title = Product.objects.filter(title__icontains=query)
                brand = Product.objects.filter(brand_name__icontains=query)
                keywords = Product.objects.filter(keywords__icontains=query)
                category = Product.objects.filter(category__title__icontains=query)
                products = title.union(brand, keywords, category)
                if products.count() == 0:
                    messages.error(
                            request, "No search results found. Please refine your search!")
            category = Category.objects.all()
            context = {'products': products, 'query': query,
                       'category': category, 'len': len(category) }
            return render(request, 'eshop/search_products.html', context)
    return HttpResponseRedirect('/')

def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        title = Product.objects.filter(title__icontains=q)
        brand = Product.objects.filter(brand_name__icontains=q)
        keywords = Product.objects.filter(keywords__icontains=q)
        category = Product.objects.filter(category__title__icontains=q)
        products = title.union(brand, keywords, category)
        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def product_detail(request,id,slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    context = {'product': product,'category': category,
               'images': images,
               }
    
    return render(request,'eshop/product-page.html',context)

# def ajaxcolor(request):
#     data = {}
#     if request.POST.get('action') == 'post':
#         size_id = request.POST.get('size')
#         productid = request.POST.get('productid')
#         colors = Variants.objects.filter(product_id=productid, size_id=size_id)
#         context = {
#             'size_id': size_id,
#             'productid': productid,
#             'colors': colors,
#         }
#         data = {'rendered_table': render_to_string('color_list.html', context=context)}
#         return JsonResponse(data)
#     return JsonResponse(data)
