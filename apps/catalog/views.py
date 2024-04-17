from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, DetailView
from django.http import HttpRequest
from .models import Catalog

class CatalogListView(ListView):
    model = Catalog
    template_name = 'catalog/index.html'
    context_object_name = 'categories'