from django.contrib import admin
from django.db.models import QuerySet

from nested_admin import NestedModelAdmin, NestedTabularInline
from mptt.admin import DraggableMPTTAdmin, TreeRelatedFieldListFilter

from .models import Topic, Quiz, Question, ChoiceAnswer, Completion


admin.site.register(Completion)

def clear_quizzes(modeladmin, request, queryset: QuerySet[Topic]) -> None:
    for topic in queryset:
        topic.quizzes.all().delete()

class ChoiceAnswerInline(NestedTabularInline):
    model = ChoiceAnswer
    extra = 1

class QuestionInline(NestedTabularInline):
    model = Question
    inlines = [ChoiceAnswerInline]
    extra = 1

@admin.register(Topic)
class TopicAdmin(DraggableMPTTAdmin):
    prepopulated_fields = {'slug': ['name']}
    list_display = ['tree_actions', 'indented_title', 'quizzes_count']
    list_display_links = ['indented_title']
    expand_tree_by_default = True
    search_fields = ['name', 'slug', 'id', 'short_description', 'description', 'parent__name']
    list_filter = [('parent', TreeRelatedFieldListFilter)]
    autocomplete_fields = ['parent']
    list_select_related = ['parent']
    actions = [clear_quizzes]
    
    fieldsets = [
        (None, {
            'fields': [('name', 'slug')], 
        }), 
        ('Extras', {
            'classes': ['collapse'], 
            'fields': ['short_description', 'description', 'image'], 
        }), 
        ('Hierarchy', {
            'fields': ['parent']
        }), 
    ]
    
    def quizzes_count(self, obj):
        return obj.get_amount_of_quizzes()

@admin.register(Quiz)
class QuizAdmin(NestedModelAdmin):
    prepopulated_fields = {'slug': ['name']}
    list_display = ['name', 'topic']
    list_display_links = ['name']
    search_fields = ['name', 'short_description', 'description', 'author__username', 'topic__name']
    list_filter = [('topic', TreeRelatedFieldListFilter), 'author']
    list_editable = ['topic']
    autocomplete_fields = ['author', 'topic']
    list_select_related = ['author', 'topic']
    inlines = [QuestionInline]
    date_hierarchy = 'created_at'

    fieldsets = [
        (None, {
            'fields': [('name', 'slug')],
        }),
        ('Extras', {
            'classes': ['collapse'],
            'fields': ['short_description', 'description'],
        }),
        ('Related', {
            'fields': ['author', 'topic']
        }),
    ]