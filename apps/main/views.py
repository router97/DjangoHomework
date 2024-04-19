from django.shortcuts import render, HttpResponse
from django.http import HttpRequest
from ..blog.models import Article
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def about(request: HttpRequest) -> HttpResponse:
    return render(request, 'about.html')

def contacts(request: HttpRequest) -> HttpResponse:
    return render(request, 'contacts.html')

def sigma(request: HttpRequest) -> HttpResponse:
    return render(request, 'sigma.html')