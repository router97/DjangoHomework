from django.contrib import admin

from .models import Catalog

@admin.register(Catalog)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
