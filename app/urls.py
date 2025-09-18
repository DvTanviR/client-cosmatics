"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from base.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home, name="home"),
    path('about/', About, name="about"),
    path('shop/', Shop, name="shop"),
    path('contact/', Contact, name="contact"),
    path('services/', Services, name="services"),
    path('product/<int:product_id>/', ProductDetail, name="product_detail"),
    path('wishlist/', Wishlist, name="wishlist"),
    path('send-quote/', SendQuote, name="send_quote"),
    path('categories/<int:category_id>/', CatagoryPage, name="category_products"),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
