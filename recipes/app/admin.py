from django.contrib import admin

# Register your models here.
from .models import Category, Recipe, Comment, MealCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'content', 'views', 'likes', 'image']
    list_filter = ['category']
    search_fields = ['title', 'category__name']
    actions = ['increase_likes', 'increase_views']

    def increase_likes(self, request, queryset):
        for recipe in queryset:
            recipe.likes += 1
            recipe.save()
    increase_likes.short_description = 'Increase likes by 1'

    def increase_views(self, request, queryset):
        for recipe in queryset:
            recipe.views += 1
            recipe.save()
    increase_views.short_description = 'Increase views by 1'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'text']
    search_fields = ['recipe__title', 'text']


@admin.register(MealCategory)
class MealCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
