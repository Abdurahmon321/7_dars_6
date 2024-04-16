from django import template
from ..models import MealCategory, Recipe
register = template.Library()


@register.simple_tag
def br_categories():
    return MealCategory.objects.filter(category=1)


@register.simple_tag
def lunch_categories():
    return MealCategory.objects.filter(category=2)


@register.simple_tag
def dinner_categories():
    return MealCategory.objects.filter(category=3)


@register.simple_tag
def all_recipes():
    return Recipe.objects.all()

