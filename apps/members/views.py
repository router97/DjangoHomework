from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def login_view(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username = username)
        except:
            pass
        
        user = authenticate(request, username = username, password = password)
        
        if user:
            login(request, user)
            
            return redirect('main:index')
    context = {}
    return render(request, 'login.html', context)

def profile_view(request: HttpRequest, username: str):
    context = {'user_context': User.objects.get(username = username)}
    return render(request, 'profile.html', context)

def logout_view(request: HttpRequest):
    
    logout(request)
    
    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)