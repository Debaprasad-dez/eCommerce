"""eCommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Buckler Admin"
admin.site.site_title = "Buckler Admin Panel"
admin.site.index_title = "Buckler Strong Room"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('eshop.urls')),
    path('eshop/', include('eshop.urls')),
    path('order/', include('order.urls')),
    path('product/', include('product.urls')),
    path('user/', include('user.urls')),
    path('', include('user.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
