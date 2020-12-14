from django.shortcuts import render, HttpResponse
from eshop.models import *
# Create your views here.
def index(request):
    return HttpResponse('Product')
