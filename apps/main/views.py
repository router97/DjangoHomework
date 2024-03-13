from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.http import HttpRequest, FileResponse
from ..blog.models import Article

def favicon(request: HttpRequest) -> FileResponse:
    file = (settings.BASE_DIR / "static" / "favicon.svg").open("rb")
    return FileResponse(file)

def index(request: HttpRequest) -> HttpResponse:
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'index.html', context)

def about(request: HttpRequest) -> HttpResponse:
    return render(request, 'about.html')

def contacts(request: HttpRequest) -> HttpResponse:
    return render(request, 'contacts.html')

def sigma(request: HttpRequest) -> HttpResponse:
    return render(request, 'sigma.html')