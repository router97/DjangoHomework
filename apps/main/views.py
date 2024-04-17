from django.shortcuts import render, HttpResponse
from django.http import HttpRequest
from ..blog.models import Article
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    article_list = Article.objects.all().select_related('author')
    paginator = Paginator(article_list, 3) 

    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
       
        articles = paginator.page(1)
    except EmptyPage:
        
        articles = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'articles': articles})

def about(request: HttpRequest) -> HttpResponse:
    return render(request, 'about.html')

def contacts(request: HttpRequest) -> HttpResponse:
    return render(request, 'contacts.html')

def sigma(request: HttpRequest) -> HttpResponse:
    return render(request, 'sigma.html')