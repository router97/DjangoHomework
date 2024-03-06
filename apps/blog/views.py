from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import HttpRequest
from .models import Article, Comment
from .forms import ArticleForm, CommentForm

def article(request: HttpRequest, id: int) -> HttpResponse:
    article = get_object_or_404(Article, id=id)
    article.views += 1
    article.save()
    form_comment = CommentForm
    context = {
        'article': article,
        'form_comment': form_comment}
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

def add_comment(request: HttpRequest, article_id: int):
    if request.method == 'POST':
        article = get_object_or_404(Article, id=article_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
    else:
        form = CommentForm() 
    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)

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

def like_comment(request: HttpRequest, comment_id: int):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.likes += 1
    comment.save()
    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)