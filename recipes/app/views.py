from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import RecipeForm, CategoryForm, CommentForm, MealCategoryForm
# Create your views here.
from .models import Recipe, Category, MealCategory


def bosh_sahifa(request):
    recipes = Recipe.objects.all()[:4]  # Eng oxirgi qo'shilgan 4 ta retseptni tanlash

    br_category = MealCategory.objects.filter(category=1)
    lunch_category = MealCategory.objects.filter(category=2)
    dinner_category = MealCategory.objects.filter(category=3)
    context = {'recipes': recipes, "br_category": br_category,
               "lunch_category": lunch_category, "dinner_category": dinner_category}
    return render(request, 'base.html', context)


""" categoriya uchun crud """


def category_list(request):
    categories = MealCategory.objects.all()
    return render(request, 'category/category_list.html', {'categories': categories})


def category_detail(request, pk):
    category = get_object_or_404(MealCategory, pk=pk)
    return render(request, 'category/category_detail.html', {'category': category})


def category_create(request):
    if request.method == 'POST':
        form = MealCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'category/category_form.html', {'form': form})


def category_update(request, pk):
    category = get_object_or_404(MealCategory, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_form.html', {'form': form})


def category_delete(request, pk):
    category = get_object_or_404(MealCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'category/category_confirm_delete.html', {'category': category})


""" recipelar uchun crud """


def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.views += 1
    recipe.save()
    comments = recipe.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.save()
            return redirect('recipe_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe, 'comments': comments, 'form': form})


def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('recipe_list')
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_form.html', {'form': form})


def recipe_update(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_list')
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/recipe_form.html', {'form': form})


def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        recipe.delete()
        return redirect('recipe_list')
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})


""" like uchun """


def like_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe.likes += 1
    recipe.save()
    return redirect('recipe_detail', recipe_id)


""" filter by category """


def filter_by_category(request, pk):
    recipes = Recipe.objects.filter(meal_category=pk)
    return render(request, 'index.html', {"recipes": recipes})


""""""


def search_results(request):
    query = request.GET.get('q')
    recipes = Recipe.objects.filter(title__icontains=query)
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

