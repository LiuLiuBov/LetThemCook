from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    quick_description = models.TextField()
    content = models.TextField()
    ingredients = models.TextField(help_text="List each ingredient on a new line.")
    picture = models.ImageField(upload_to='recipes/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')

    def __str__(self):
        return self.title

class Review(models.Model):
    content = models.TextField()
    rating = models.IntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f"Review by {self.user.username} for {self.recipe.title}"

