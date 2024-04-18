from django.contrib import admin

from .models import Catalog, Product


class ProductCategoryInline(admin.TabularInline):
    model = Product.category.through
    extra = 1

@admin.register(Catalog)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'image')
    search_fields = ('name', 'description')
    list_filter = ('parent',)
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'image')
        }),
        ('Hierarchy', {
            'fields': ('parent',)
        }),
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category',)
    inlines = (ProductCategoryInline,)