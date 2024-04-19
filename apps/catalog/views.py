from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Catalog, Product


class CatalogListView(ListView):
    model = Catalog
    template_name = 'catalog/index.html'
    context_object_name = 'categories' 
    
    def get_queryset(self):
        return Catalog.objects.filter(parent=None)

class ProductByCategoryView(ListView):
    template_name = 'catalog/product_by_category.html'
    context_object_name = 'products'

    # FIXME: 3i9ewokfmdnjgi
    def get_queryset(self):
        category_slug = self.kwargs['slug']
        category = get_object_or_404(Catalog, slug=category_slug)
        descendants = category.get_descendants(include_self=True)
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