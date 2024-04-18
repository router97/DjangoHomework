from django.contrib import admin

from .models import Article, Comment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    search_fields = ('title', 'content', 'author__username')
    list_filter = ('author',)
    readonly_fields = ('created_at', 'edited_at')
    
    fieldsets = (
        (None, {
            'fields': ('author', 'title', 'content', 'image')
        }),
        ('Date Information', {
            'fields': ('created_at', 'edited_at'),
        }),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'article', 'author')
    search_fields = ('content', 'author__username')
    list_filter = ('author', 'created_at')
    readonly_fields = ('created_at', 'edited_at')
    
    fieldsets = (
        (None, {
            'fields': ('article', 'author', 'content')
        }),
        ('Date Information', {
            'fields': ('created_at', 'edited_at'),
        }),
    )