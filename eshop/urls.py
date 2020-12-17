from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('', views.index, name="home"),
    path('aboutus/', views.aboutus, name="aboutus"),
    path('contact/', views.contactus, name="contact"),
    path('category/<int:id>/<slug:slug>', views.category_products, name="category_product"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)