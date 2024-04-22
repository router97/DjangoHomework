from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.http import HttpRequest
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CartAddProductForm


class AddToCartView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponseRedirect:
        data = request.GET.copy()
        data.update(user=request.user)
        request.GET = data
        
        form = CartAddProductForm(request.GET)
        
        if form.is_valid():
            cart = form.save()
            return redirect('catalog:product', slug=cart.product.slug, category_slug=cart.product.main_category().slug)
            
        

def cart(request: HttpRequest):
    return render(request, 'cart.html')