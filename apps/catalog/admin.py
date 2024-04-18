from django.contrib import admin

from .models import Catalog


@admin.register(Catalog)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'image')
    search_fields = ('name', 'description')
    list_filter = ('parent',)
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'image')
        }),
        ('Hierarchy', {
            'fields': ('parent',)
        }),
    )