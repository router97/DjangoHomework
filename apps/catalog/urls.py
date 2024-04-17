from django.urls import path

from .views import CatalogListView

app_name = 'catalog'

urlpatterns = [
    path('', CatalogListView.as_view(), name='index'),
    path('<slug:slug>/', CatalogListView.as_view(), name='category')
]