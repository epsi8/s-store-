from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('category/<slug:slug>/', views.category_list, name='category_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('review/<slug:slug>/', views.add_review, name='add_review'),
]
