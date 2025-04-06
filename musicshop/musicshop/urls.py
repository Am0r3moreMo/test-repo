"""
URL configuration for musicshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.urls import path
from main.views import PickUpPointView, ProductListAPIView, ProductDetailAPIView, CartItemView, SignUpView, SignInView
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("products", ProductListAPIView.as_view(), name="product-list"),
    path("products/<int:pk>", ProductDetailAPIView.as_view(), name="product-detail"),
    path("pickup-points", PickUpPointView.as_view(), name="pickup-list"),
    path("cart", CartItemView.as_view(), name="cart-item-create"),
    path("signin", SignInView.as_view(), name="signin"),
    path("signup", SignUpView.as_view(), name="signup"),
    # path("cart/", CartView.as_view(), name="pickup-list"),
]
