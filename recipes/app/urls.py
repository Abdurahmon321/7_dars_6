from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.bosh_sahifa, name="index"),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/create/', views.recipe_create, name='recipe_create'),
    path('recipe/<int:pk>/update/', views.recipe_update, name='recipe_update'),
    path('recipe/<int:pk>/delete/', views.recipe_delete, name='recipe_delete'),

    path('recipe_filter/<int:pk>', views.filter_by_category, name="recipe_filter_by"),

    path('recipe/<int:recipe_id>/like/', views.like_recipe, name='like_recipe'),

    path('search/', views.search_results, name='search_results'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
