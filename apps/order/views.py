from django.db.models.base import Model as Model
from django.http import HttpRequest
from django.contrib import messages
from django.shortcuts import redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, DeleteView
from django.db.models.query import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CartAddProductForm
from .models import Cart, CartProduct


class AddToCartView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponseRedirect:
        data = request.GET.copy()
        data['cart'] = request.user.cart
        request.GET = data
        
        form = CartAddProductForm(request.GET)
        
        if form.is_valid():
            cart = form.save()
            return redirect('catalog:product', slug=cart.product.slug, category_slug=cart.product.main_category().slug)

class RemoveFromCartView(LoginRequiredMixin, DeleteView):
    model = CartProduct
    success_url = reverse_lazy('order:cart')
    
    def get_object(self, queryset: QuerySet | None = None) -> CartProduct:
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.get(product=self.kwargs['id'])

class CartDetailView(LoginRequiredMixin, DetailView):
    model = Cart
    template_name = 'order/cart.html'
    context_object_name = 'cart'
    
    def get_object(self, queryset: QuerySet | None = None) -> Cart:
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.get(user=self.request.user)
