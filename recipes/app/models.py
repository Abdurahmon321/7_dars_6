from django.contrib.auth.models import User
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
    author = models.ForeignKey(User, on_delete=models.CASCADE)

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


class UserProfile(models.Model):
        img = models.ImageField(upload_to="user/", null=True, blank=True)
        status = models.CharField(max_length=150, null=True, blank=True)
        address = models.CharField(max_length=255, null=True, blank=True)
        phone = models.CharField(max_length=15, null=True, blank=True)
        mobile = models.CharField(max_length=15, null=True, blank=True)
        sayt = models.URLField(max_length=250, null=True, blank=True)
        github = models.CharField(max_length=250, null=True, blank=True)
        instragram = models.CharField(max_length=250, null=True, blank=True)
        telegram = models.CharField(max_length=250, null=True, blank=True)
        facebook = models.CharField(max_length=250, null=True, blank=True)
        user = models.OneToOneField(User, on_delete=models.CASCADE)

        def __str__(self):
            return f"{ self.user.username }"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.message}"