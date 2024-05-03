from django.contrib import admin

from nested_admin import NestedTabularInline, NestedModelAdmin
from mptt.admin import MPTTModelAdmin, TreeRelatedFieldListFilter

from .models import Topic, Quiz, Question, ChoiceAnswer


@admin.register(Topic)
class TopicAdmin(MPTTModelAdmin):
    prepopulated_fields = {'slug': ['name']}
    list_display = ['name', 'image_tag']
    list_display_links = ['name']
    search_fields = [
        'name', 
        'slug', 
        'id', 
        'short_description', 
        'description', 
        'parent__name', 
    ]
    list_filter = [
        ('parent', TreeRelatedFieldListFilter)
    ]
    autocomplete_fields = ['parent']
    list_select_related = ['parent']
    fieldsets = [
        (
            None, 
            {
                'fields': [('name', 'slug')], 
            }, 
        ), 
        (
            'Extras', 
            {
                'classes': ['collapse'], 
                'fields': ['short_description', 'description', 'image'], 
            }, 
        ), 
        (
            'Hierarchy', 
            {
                'fields': ['parent']
            }, 
        ), 
    ]

class ChoiceAnswerInline(NestedTabularInline):
    model = ChoiceAnswer
    extra = 1

class QuestionInline(NestedTabularInline):
    model = Question
    inlines = [ChoiceAnswerInline]
    extra = 1

@admin.register(Quiz)
class QuizAdmin(NestedModelAdmin):
    prepopulated_fields = {'slug': ['name']}
    
    list_display = ['name', 'topic']
    list_display_links = ['name']
    
    search_fields = [
        'name', 
        'short_description', 
        'description', 
        'author__username', 
        'topic__name', 
    ]
    
    list_filter = [
        ('topic', TreeRelatedFieldListFilter), 
        'author', 
    ]
    list_editable = ['topic']
    
    autocomplete_fields = ['author', 'topic']
    
    list_select_related = ['author', 'topic']
    
    inlines = [QuestionInline]
    date_hierarchy = 'created_at'

    fieldsets = [
        (
            None, 
            {
                'fields': [('name', 'slug')], 
            },
        ),
        (
            'Extras', 
            {
                'classes': ['collapse'], 
                'fields': ['short_description', 'description'], 
            },
        ),
        (
            'Related', 
            {
                'fields': ('author', 'topic')
            },
        ),
    ]