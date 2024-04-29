from uuid import UUID

from django.http import HttpRequest, HttpResponseBadRequest
from django.contrib import messages
from django.shortcuts import redirect, HttpResponseRedirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, DeleteView
from django.db.models.query import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CartAddProductForm
from .models import Cart, CartProduct
from ..catalog.models import Product


class CartDetailView(LoginRequiredMixin, DetailView):
    model = Cart
    template_name = 'order/cart.html'
    context_object_name = 'cart'
    
    def get_object(self, queryset: QuerySet | None = None) -> Cart:
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.get(user=self.request.user)

class RemoveFromCartView(LoginRequiredMixin, DeleteView):
    model = CartProduct
    success_url = reverse_lazy('order:cart')
    
    def get_object(self, queryset: QuerySet | None = None) -> CartProduct:
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.get(product=self.kwargs['id'], cart__user=self.request.user)

class AddToCartView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponseRedirect:
        data = request.GET.copy()
        data['cart'] = request.user.cart
        request.GET = data
        
        form = CartAddProductForm(request.GET)
        
        if form.is_valid():
            cart_product: CartProduct = form.save()
            product: Product = cart_product.product
            messages.success(request, f'Successfully added {product.name}')
            return redirect('catalog:product', slug=product.slug, category_slug=product.main_category().slug)
        
        messages.error(request, 'Failed to add product to cart.')

class ProductQuantityChangeView(LoginRequiredMixin, View):
    """A view to handle changes in product quantity in the user's cart."""
    
    def post(self, request: HttpRequest, id: UUID) -> HttpResponseRedirect:
        cart_product: CartProduct = get_object_or_404(
            CartProduct, 
            cart__user=request.user, 
            product__id=id
        )
        
        new_quantity_str = request.POST.get(f'change_quantity{id}')
        if not new_quantity_str.isdigit():
            return HttpResponseBadRequest("Invalid quantity")
        
        new_quantity: int = int(new_quantity_str)
        max_quantity: int = cart_product.product.quantity
        
        if new_quantity <= 0:
            cart_product.delete()
        else:
            cart_product.quantity = min(new_quantity, max_quantity)
            cart_product.save(update_fields=['quantity'])
        
        return redirect('order:cart')