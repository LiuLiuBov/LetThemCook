import os
import django
import random
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'letthemcookproject.settings')
django.setup()

from django.contrib.auth.models import User
from letthemcookapp.models import Recipe, Save, Review

image_path = os.path.join(os.path.dirname(__file__), 'media')
image_filenames = ['spaghetti.png', 'banana_bread.png']

def get_image_path(filename):
    return os.path.join(image_path, filename)

def populate():
    # Users
    user_names = ['Alice', 'Bob', 'Charlie', 'Diana']
    users = []

    for name in user_names:
        user, created = User.objects.get_or_create(username=name, email=f"{name}@example.com")
        if created:
            user.set_password('1234')
            user.save()
        users.append(user)


    # Recipes
    recipes_data = [
        {
            "title": "Classic Tomato Spaghetti",
            "quick_description": "Simple and classic spaghetti with tomato sauce.",
            "content": "Boil pasta, prepare sauce with tomatoes, onions, and garlic.",
            "ingredients": "Spaghetti\nTomatoes\nOnion\nGarlic\nOlive Oil\nSalt\nPepper",
            "picture": get_image_path(image_filenames[0]),
            "user": users[0]
        },
        {
            "title": "Banana Bread",
            "quick_description": "Moist and delicious banana bread.",
            "content": "Mix mashed bananas with flour, sugar, and butter, then bake.",
            "ingredients": "Bananas\nFlour\nSugar\nButter\nEggs\nBaking Soda\nSalt",
            "picture": get_image_path(image_filenames[1]),
            "user": users[1]
        }
    ]

    for recipe_data in recipes_data:
        recipe, created = Recipe.objects.get_or_create(
            title=recipe_data['title'],
            defaults=recipe_data
        )

    # Saves
    for user in users:
        for recipe in Recipe.objects.all():
            if random.choice([True, False]):
                Save.objects.get_or_create(user=user, recipe=recipe)

    # Reviews
    review_data = [
        {"recipe": Recipe.objects.get(title="Classic Tomato Spaghetti"), "user": users[2], "rating": 5, "comment": "Absolutely love this classic recipe!"},
        {"recipe": Recipe.objects.get(title="Banana Bread"), "user": users[3], "rating": 4, "comment": "Really good, but a bit too sweet for me."}
    ]

    for review in review_data:
        Review.objects.get_or_create(
            recipe=review['recipe'],
            user=review['user'],
            defaults={
                'rating': review['rating'],
                'comment': review['comment'],
                'created_at': datetime.now()
            }
        )

if __name__ == '__main__':
    print("Starting population script...")
    populate()
    print("Finished populating database with realistic data.")
