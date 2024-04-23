from django.shortcuts import render, HttpResponse
from django.http import HttpRequest


def about(request: HttpRequest) -> HttpResponse:
    return render(request, 'about.html')

def custom_404(request, exception):
    return render(request, '404.html', status=404)