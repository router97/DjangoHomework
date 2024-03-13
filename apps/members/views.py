from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegisterForm, ProfileForm

def login_view(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if request.method != 'POST':
        return render(request, 'login.html')
    
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    user = authenticate(request, username = username, password = password)
    
    if not user:
        messages.error(request, 'Login failed')
        return redirect('members:login')
    
    login(request, user)
    messages.success(request, 'Logged in successfully')
    return redirect('main:index')

def register_view(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    context = {'form': RegisterForm()}
    
    if request.method != 'POST':
        return render(request, 'register.html', context)

    form = RegisterForm(request.POST)
    
    if not form.is_valid():
        messages.error(request, 'Register failed')
        context.update({'form': form})
        return render(request, 'register.html', context)
    
    user = form.save()
    login(request, user)
    
    return redirect('main:index')

def profile_view(request: HttpRequest, username: str) -> HttpResponse | HttpResponseRedirect:
    requested_user = get_object_or_404(User, username=username)
    context = {'user_context': requested_user}
    
    if request.method != 'POST':
        return render(request, 'profile.html', context)
    
    if request.user == requested_user:
        form = ProfileForm(request.POST, instance = requested_user)
        
        if form.is_valid():
            messages.success(request, 'Successfully updated profile')
            form.save()
        else:
            messages.error(request, "Failed to update profile")
            return render(request, 'profile.html', context)

        return redirect('members:profile', username=requested_user.username)

def logout_view(request: HttpRequest) -> HttpResponseRedirect:
    logout(request)
    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)