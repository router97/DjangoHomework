from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, HttpResponseRedirect
from django.http import HttpRequest
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Article, Comment
from .forms import ArticleForm, CommentForm


def article(request: HttpRequest, id: int) -> HttpResponse:
    article = get_object_or_404(Article.objects.select_related('author').prefetch_related('comments__author'), id=id)
    article.views += 1
    article.save(update_fields=('views',))
    form_comment = CommentForm()
    all_comments = article.comments.all()

    paginator = Paginator(all_comments, 10)  
    page_number = request.GET.get('page')
    try:
        comments = paginator.page(page_number)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context = {
        'article': article,
        'form_comment': form_comment,
        'comments': comments,
    }
    return render(request, 'article.html', context)

class AddArticleView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {'form': ArticleForm()}
        return render(request, 'article_form.html', context)
    
    def post(self, request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
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

class EditArticleView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
        article = get_object_or_404(Article.objects.select_related('author'), id=id)
        
        if request.user != article.author:
            messages.error(request, 'You are not the author of this article')
            next_url = request.META.get('HTTP_REFERER', '/')
            return redirect(next_url)
        
        form = ArticleForm(instance=article)
        context = {'form': form}
        return render(request, 'article_form.html', context)
    
    def post(self, request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
        article = get_object_or_404(Article.objects.select_related('author'), id=id)
    
        if request.user != article.author:
            messages.error(request, 'You are not the author of this article')
            next_url = request.META.get('HTTP_REFERER', '/')
            return redirect(next_url)
        
        form = ArticleForm(request.POST, request.FILES, instance=article)
    
        if not form.is_valid():
            context = {'form': form}
            messages.error(request, 'Failed to edit the article')
            return render(request, 'article_form.html', context)
        
        form.save()
        messages.success(request, f'Edited article {article.id} successfully')
        return redirect('blog:article', id=article.id)

@login_required
@require_POST
def add_comment(request: HttpRequest, article_id: int):
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
def like_article(request: HttpRequest, article_id: int) -> HttpResponseRedirect:
    article = get_object_or_404(Article, id=article_id)
    article.likes += 1
    article.save()
    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)

@login_required
def dislike_article(request: HttpRequest, article_id: int) -> HttpResponseRedirect:
    article = get_object_or_404(Article, id=article_id)
    article.dislikes += 1
    article.save(update_fields=('dislikes',))
    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)

@login_required
def like_comment(request: HttpRequest, comment_id: int) -> HttpResponseRedirect:
    comment = get_object_or_404(Comment, id=comment_id)
    comment.likes += 1
    comment.save(update_fields=('likes',))
    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)

def index(request):
    article_list = Article.objects.all().select_related('author')
    paginator = Paginator(article_list, 12) 

    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
       
        articles = paginator.page(1)
    except EmptyPage:
        
        articles = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'articles': articles})