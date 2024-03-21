from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import numpy as np

class Recipe(models.Model):
    
    title = models.CharField(max_length=255)
    quick_description = models.TextField()
    content = models.TextField()
    ingredients = models.TextField(help_text="List each ingredient on a new line.")
    saves = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0)
    picture = models.ImageField(upload_to='', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')

    def update_average(self):
        print("updating average")
        reviews = Review.objects.filter(recipe=self)
        if reviews.exists():
            self.average_rating = np.mean([review.rating for review in reviews])
        else:
            self.average_rating=0
        self.save()
    
    def update_saves(self):
        saves = Save.objects.filter(recipe=self)
        self.saves = len(saves)
        self.save()

    def __str__(self):
        return self.title

class Save(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # user cannot save the same recipe more than once.
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"{self.user.username} saved {self.recipe.title}"

class Review(models.Model):

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # restrict users from reviewing the same recipe multiple times.
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"Review by {self.user.username} for {self.recipe.title}"