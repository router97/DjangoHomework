from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect


def about(request: HttpRequest) -> HttpResponse:
    return render(request, 'about.html')

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def index(request: HttpRequest) -> HttpResponseRedirect:
    return redirect('blog:index')