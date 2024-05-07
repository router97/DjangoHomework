from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib.auth.models import User
from django.db.models import QuerySet

from .forms import RegisterForm, ProfileForm
from ..quiz.models import Topic

class LoginView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'login.html')
    
    def post(self, request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username = username, password = password)
        
        if not user:
            messages.error(request, 'Login failed.')
            return redirect('members:login')
        
        login(request, user)
        messages.info(request, f'Welcome Back, {username}!')
        return redirect('blog:index')

class RegisterView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {'form': RegisterForm()}
        return render(request, 'register.html', context)
    
    def post(self, request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
        form = RegisterForm(request.POST)
    
        if not form.is_valid():
            messages.error(request, 'Register failed')
            context = {'form': form}
            return render(request, 'register.html', context)
        
        user = form.save()
        login(request, user)
        messages.info(request, f'Welcome, {form.cleaned_data['username']}!')
        return redirect('blog:index')

class ProfileView(View):
    def get(self, request: HttpRequest, username: str) -> HttpResponse:
        requested_user: User = get_object_or_404(User.objects, username=username)
        all_topics: QuerySet[Topic] = Topic.objects.filter()
        
        topics_with_completions = []
        for topic in all_topics:
            completion = round(topic.get_topic_completion(requested_user.id))
            
            if completion:
                topic.completion = completion
                topics_with_completions.append(topic)
        
        
        context = {
            'user_context': requested_user, 
            'quiz_topics_in_progress': topics_with_completions, 
        }
        return render(request, 'profile.html', context)
    
    def post(self, request: HttpRequest, username: str) -> HttpResponse | HttpResponseRedirect:
        requested_user = get_object_or_404(User, username=username)
        
        if request.user != requested_user:
            return
        
        form = ProfileForm(request.POST, instance = requested_user)
        
        if form.is_valid():
            messages.success(request, 'Successfully updated profile')
            form.save()
        else:
            messages.error(request, "Failed to update profile")

        return redirect('members:profile', username=requested_user.username)

def logout_view(request: HttpRequest) -> HttpResponseRedirect:
    logout(request)
    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)