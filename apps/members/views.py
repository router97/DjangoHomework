from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import authenticate, login, logout
from .forms import ProfileForm

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
    requested_user = User.objects.get(username = username)
    
    context = {'user_context': requested_user}
    
    if request.method == 'POST' and request.user == requested_user:
        
        form = ProfileForm(request.POST, instance = requested_user)
        
        if form.is_valid():
            form.save()
        else:
            return render(request, 'profile.html', context)
        
        context.update({'user_context': requested_user})
        
        return redirect(reverse('members:profile', kwargs={'username': requested_user.username}))
        
    return render(request, 'profile.html', context)

def logout_view(request: HttpRequest):
    
    logout(request)
    
    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)