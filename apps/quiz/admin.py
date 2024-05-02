from django.contrib import admin

from .models import Topic, Quiz, Question, ChoiceAnswer, Completion

from nested_admin import NestedTabularInline, NestedModelAdmin

admin.site.register(Completion)

class ChoiceAnswerInline(NestedTabularInline):
    model = ChoiceAnswer
    extra = 1

class QuestionInline(NestedTabularInline):
    model = Question
    inlines = [ChoiceAnswerInline]
    extra = 1

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'image_tag')
    search_fields = ('name', 'short_description', 'description')
    list_filter = ('parent',)
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'short_description', 'description', 'image')
        }),
        ('Hierarchy', {
            'fields': ('parent',)
        }),
    )
    
@admin.register(Quiz)
class QuizAdmin(NestedModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'topic')
    search_fields = ('name', 'short_description', 'description')
    list_filter = ('topic', 'author')
    inlines = [QuestionInline]

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'short_description', 'description')
        }),
        (None, {
            'fields': ('author', 'topic')
        }),
    )