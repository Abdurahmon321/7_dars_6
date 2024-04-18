from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.models import User

from .forms import RecipeForm, CategoryForm, CommentForm, MealCategoryForm, UserLoginForm, UserSignupForm, \
    UserProfileForm, MessageForm
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
# Create your views here.
from .models import Recipe, Category, MealCategory, UserProfile, Message


def bosh_sahifa(request):
    recipes = Recipe.objects.all()[:4]  # Eng oxirgi qo'shilgan 4 ta retseptni tanlash
    user = User.objects.all()

    context = {'recipes': recipes}
    return render(request, 'base.html', context)


""" categoriya uchun crud """


def category_list(request):
    categories = MealCategory.objects.all()
    return render(request, 'category/category_list.html', {'categories': categories})


def category_detail(request, pk):
    category = get_object_or_404(MealCategory, pk=pk)
    return render(request, 'category/category_detail.html', {'category': category})


@permission_required("app.add_meal_category", login_url='index')
def category_create(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = MealCategoryForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Categoriya yaratildi")
                return redirect('category_list')
        else:
            form = CategoryForm()
        return render(request, 'category/category_form.html', {'form': form})
    else:
        return HttpResponse("Sizda ruxsat yo'q")


@permission_required("app.change_meal_category", login_url="index")
def category_update(request, pk):
    if request.user.is_superuser:
        category = get_object_or_404(MealCategory, pk=pk)
        if request.method == 'POST':
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                messages.success(request, "Categoriya o'zgartirildi")
                return redirect('category_list')
        else:
            form = CategoryForm(instance=category)
        return render(request, 'category/category_form.html', {'form': form})
    else:
        return HttpResponse("Sizda ruxsat yo'q")


@permission_required("app.delete_meal_category", login_url="index")
def category_delete(request, pk):
    if request.user.is_superuser:
        category = get_object_or_404(MealCategory, pk=pk)
        if request.method == 'POST':
            category.delete()
            messages.success(request, "Categoriya o'chirildi")
            return redirect('category_list')
        return render(request, 'category/category_confirm_delete.html', {'category': category})
    else:
        return HttpResponse("Sizda ruxsat yo'q")


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
            messages.success(request, " Comment qo'shildi")
            return redirect('recipe_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe, 'comments': comments, 'form': form})


@permission_required("app.add_recipe", login_url="index")
def recipe_create(request):

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, 'Recipe yaratildi')
            return redirect('recipe_list')
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_form.html', {'form': form})


@permission_required("app.change_recipe", login_url="index")
def recipe_update(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, "Recipe o'zgartirildi")
            return redirect('recipe_list')
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/recipe_form.html', {'form': form})


@permission_required("app.delete_recipe", login_url="index")
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, "Recipe o'chirildi")
        return redirect('recipe_list')
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})


""" like uchun """


def like_recipe(request, recipe_id):
    if request.user.is_authenticated:
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        recipe.likes += 1
        recipe.save()
        return redirect('recipe_detail', recipe_id)
    else:
        return redirect('login')


""" filter by category """


def filter_by_category(request, pk):
    recipes = Recipe.objects.filter(meal_category=pk)
    return render(request, 'index.html', {"recipes": recipes})


""""""


def search_results(request):
    query = request.GET.get('q')
    recipes = Recipe.objects.filter(title__icontains=query)
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Saytga xush kelibsiz! {user.username}")
            return redirect('index')

        if form.errors:
            for error in form.error_messages.values():
                messages.error(request, str(error))
    return render(request, 'user/login.html')


def user_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Muvaffaqiyatli ro'yxatdan o'tdingiz. Endi kiring.")
            return redirect('login')
    else:
        form = UserSignupForm()

    context = {
        'form': form,
        'title': 'Sign up'
    }
    return render(request, 'user/signup.html', context)


def user_logout(request):
    logout(request)
    messages.warning(request, "Siz saytdan chiqdingiz!!!")
    return redirect('login')


def account_info(request, username):
    try:
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user_id=user.id)
        context = {
            "user": user,
            "user_profile": user_profile,
            "title": f"{user.username} profili "
        }
    except UserProfile.DoesNotExist:
        # UserProfile topilmaganida, bo'sh obyekt yaratamiz
        user_profile = UserProfile.objects.create(user=user)
        context = {
            "user": user,
            "user_profile": user_profile,
            "title": f"{user.username} profili "
        }
    return render(request, "user/user_profile.html", context)


def user_profile_edit(request):
    if request.user:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = None

        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
            if form.is_valid():
                user_profile = form.save(commit=False)
                user_profile.user = request.user
                user_profile.save()
                return redirect('index')
        else:
            form = UserProfileForm(instance=user_profile)

        return render(request, 'user/user_profile_form.html', {'form': form})
    else:
        return HttpResponse("Page not found")


def user_profile_create(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('index')
    else:
        form = UserProfileForm()

    return render(request, 'user/user_profile_form.html', {'form': form})


"""Message uchun """


def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('inbox')  # Yuborilgan xabarlar ro'yxati
    else:
        form = MessageForm()
    return render(request, 'send_message.html', {'form': form})


def inbox(request):
    received_messages = Message.objects.filter(receiver=request.user)
    return render(request, 'inbox.html', {'messages': received_messages})
