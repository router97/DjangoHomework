from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
    path('add/', views.AddToCartView.as_view(), name='add_to_cart'), 
    path('cart/', views.cart, name='cart'), 
]