from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MealCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    meal_category = models.ForeignKey(MealCategory, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='recipe_images/')

    def __str__(self):
        return self.title

    def increase_likes(self):
        self.likes += 1
        self.save()

    def increase_views(self):
        self.views += 1
        self.save()


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()

    def __str__(self):
        return f"Comment by {self.recipe.title}"
