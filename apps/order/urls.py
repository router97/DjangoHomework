from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
    path('add/', views.AddToCartView.as_view(), name='add_to_cart'), 
    path('cart/', views.CartDetailView.as_view(), name='cart'), 
    path('cart/remove/<uuid:id>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'), 
    path('cart/change_quantity/<uuid:id>/', views.ProductQuantityChangeView.as_view(), name='change_quantity'), 
]