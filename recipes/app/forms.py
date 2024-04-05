from django import forms
from .models import Recipe, Category, Comment, MealCategory


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['category', 'meal_category', 'title', 'content', 'image']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class MealCategoryForm(forms.ModelForm):
    class Meta:
        model = MealCategory
        fields = ['name', 'category']
