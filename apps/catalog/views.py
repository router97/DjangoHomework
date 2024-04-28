from typing import Any
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Catalog, Product
from ..order.models import Cart, CartProduct


class CatalogListView(ListView):
    model = Catalog
    template_name = 'catalog/index.html'
    context_object_name = 'categories' 
    
    def get_queryset(self):
        return Catalog.objects.filter(parent=None)

class ProductByCategoryView(ListView):
    template_name = 'catalog/product_by_category.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        category = self.kwargs.get('slug')
        descendants = Catalog.objects.filter(slug=category).get_descendants(include_self=True)
        queryset = Product.objects.filter(category__in=descendants).prefetch_related('category')
        return queryset

    # FIXME: weurjnsfm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs['slug']
        category = get_object_or_404(Catalog, slug=category_slug)
        context['category'] = category
        context['categories'] = Catalog.objects.filter(parent=category)
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart: Cart = self.request.user.cart
        
        context['in_cart'] = not cart.products.filter(product__slug=self.kwargs['slug']).exists()
        return context