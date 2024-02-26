from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.http import HttpRequest, FileResponse

def favicon(request: HttpRequest) -> FileResponse:
    print('asking for fav')
    file = (settings.BASE_DIR / "static" / "favicon.svg").open("rb")
    return FileResponse(file)

def index(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, 'index.html', context)

def about(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, 'about.html', context)

def contacts(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, 'contacts.html', context)

def sigma(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, 'sigma.html', context)