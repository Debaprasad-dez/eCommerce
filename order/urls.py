from django.urls import path
from . import views
urlpatterns = [
    # path('', views.index, name="Order"),
    path('addtoshopcart/<int:id>', views.addtoshopcart, name="addtoshopcart"),
    path('deletefromcart/<int:id>', views.deletefromcart, name="deletefromcart"),
    path('shopcart/', views.shopcart, name="shopcart"),
    path('orderproduct/', views.orderproduct, name='payu_demo'),
    path('success', views.payu_success, name='success'),
    path('failure', views.payu_failure, name='failure'),
]