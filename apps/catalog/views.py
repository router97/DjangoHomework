# from django.shortcuts import render, HttpResponse
# from django.http import HttpRequest
from django.views.generic import ListView, DetailView

from .models import Catalog, Product


class CatalogListView(ListView):
    model = Catalog
    template_name = 'catalog/index.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return super().get_queryset().select_related('parent').prefetch_related('child')
        # return Catalog.objects.filter(parent=None).select_related('parent').prefetch_related('child')
    
class ProductByCategoryView(DetailView):
    model = Catalog
    template_name = 'catalog/product_by_category.html'
    context_object_name = 'category'