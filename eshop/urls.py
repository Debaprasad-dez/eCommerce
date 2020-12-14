from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="home"),
    path('aboutus/', views.aboutus, name="aboutus"),
    path('contact/', views.contactus, name="contact"),
    path('category/<int:id>/<slug:slug>', views.category_products, name="category_product"),
]
