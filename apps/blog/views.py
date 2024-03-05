from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import HttpRequest
from .models import Article
from .forms import ArticleForm

def article(request: HttpRequest, id: int) -> HttpResponse:
    article = get_object_or_404(Article, id=id)
    article.views += 1
    article.save()
    context = {'article': article}
    return render(request, 'article.html', context)

def add_article(request: HttpRequest):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main:index')  
    else:
        form = ArticleForm()  
    context = {'form': form}
    return render(request, 'article_form.html', context)

def like(request: HttpRequest, article_id: int):
    article = get_object_or_404(Article, id=article_id)
    article.likes += 1
    article.save()
    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)

def dislike(request: HttpRequest, article_id: int):
    article = get_object_or_404(Article, id=article_id)
    article.dislikes += 1
    article.save()
    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)