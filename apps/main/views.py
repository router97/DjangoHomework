from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def lolasdasdasd(request):
    return HttpResponse('<h1>LOL</h1>')

def about(request):
    return render(request, 'main/about.html')