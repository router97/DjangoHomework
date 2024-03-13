from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from .models import Article, Comment
from django.contrib import messages
from .forms import ArticleForm, CommentForm

def article(request: HttpRequest, id: int) -> HttpResponse:
    article = get_object_or_404(Article, id=id)
    article.views += 1
    article.save()
    form_comment = CommentForm()
    context = {
        'article': article,
        'form_comment': form_comment
    }
    return render(request, 'article.html', context)

@login_required
def add_article(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    
    if request.method != 'POST':
        form = ArticleForm() 
        context = {'form': form}
        return render(request, 'article_form.html', context)
    
    form = ArticleForm(request.POST, request.FILES)
    
    if not form.is_valid():
        messages.error(request, 'Failed to create article')
        context = {'form': form}
        return render(request, 'article_form.html', context)
    
    article = form.save(commit=False)
    article.author = request.user
    article.save()
    messages.success(request, 'Created article')
    return redirect('blog:article', id=article.id)  

@login_required
def delete_article(request: HttpRequest, id: int):
    article = get_object_or_404(Article, id=id)
    
    if request.user != article.author:
        messages.error(request, 'You are not the author of this article')
    else:
        messages.success(request, f'Sucessfully deleted article "{article.title}"')
        article.delete()
    
    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)
    
@login_required
def edit_article(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    article = get_object_or_404(Article, id=id)
    
    if request.user != article.author:
        messages.error(request, 'You are not the author of this article')
        next_url = request.META.get('HTTP_REFERER', '/')
        return redirect(next_url)
    
    if request.method != 'POST':
        form = ArticleForm(instance=article)
        context = {'form': form}
        return render(request, 'article_form.html', context)

    form = ArticleForm(request.POST, request.FILES, instance=article)
    
    if not form.is_valid():
        context = {'form': form}
        messages.error(request, 'Failed to edit the article')
        return render(request, 'article_form.html', context)
    
    form.save()
    messages.success(request, f'Edited article {article.id} successfully')
    return redirect('blog:article', id = article.id)

@login_required
def add_comment(request: HttpRequest, article_id: int):
    if request.method != 'POST':
        form = CommentForm
    
    else:
        article = get_object_or_404(Article, id=article_id)
        form = CommentForm(request.POST)
        
        if not form.is_valid():
            messages.error(request, 'Failed to add comment')
            
        else:
            messages.success(request, 'Added comment sucessfully')
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
    
    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)

@login_required
def like(request: HttpRequest, article_id: int) -> HttpResponseRedirect:
    article = get_object_or_404(Article, id=article_id)
    article.likes += 1
    article.save()
    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)

@login_required
def dislike(request: HttpRequest, article_id: int) -> HttpResponseRedirect:
    article = get_object_or_404(Article, id=article_id)
    article.dislikes += 1
    article.save()
    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)

@login_required
def like_comment(request: HttpRequest, comment_id: int) -> HttpResponseRedirect:
    comment = get_object_or_404(Comment, id=comment_id)
    comment.likes += 1
    comment.save()
    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)