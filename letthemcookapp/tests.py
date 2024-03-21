from django.test import TestCase
from django.contrib.auth.models import User
from .models import Recipe, Review, Save

# Create your tests here.

class RecipeModelTest(TestCase):

    #tests 'average_rating' field of recipe is updated

    def test_update_average(self):
        user1 = User.objects.create_user(user='testuser', email='testuser@eg.com', password='testpassword')
        user2 = User.objects.create_user(user='testuser2', email='testuser2@eg.com', password='testpassword2')
        recipe = Recipe.objects.create(title='Test Recipe', quick_description='Test description', content='Test recipe content', ingredients='Test recipe ingredients')
        review1 = Review.objects.create(recipe=recipe, user=user1, rating=5, comment='very good')
        review2 = Review.objects.create(recipe=recipe, user=user2, rating=4, comment='good')

        recipe.refresh_from_db()
        self.assertEqual(recipe.average_rating, 4.5)

    #test 'saves' field of recipe is updated when recipe is saved

    def test_update_saves(self):
        user1 = User.objects.create_user(user='testuser', email='testuser@eg.com', password='testpassword')
        user2 = User.objects.create_user(user='testuser2', email='testuser2@eg.com', password='testpassword2')
        recipe = Recipe.objects.create(title='Test Recipe', quick_description='Test description', content='Test recipe content', ingredients='Test recipe ingredients')
        save1 = Save.objects.create(user=user1, recipe=recipe)
        save2 = Save.objects.create(user=user2, recipe=recipe)

        recipe.refresh_from_db()
        self.assertEqual(recipe.saves, 2)

class SaveModelTest(TestCase):

    #tests a user cannot save the same recipe mutiple times

    def test_unique_together(self):
        user1 = User.objects.create_user(user='testuser', email='testuser@eg.com', password='testpassword')
        recipe = Recipe.objects.create(title='Test Recipe', quick_description='Test description', content='Test recipe content', ingredients='Test recipe ingredients')
        Save.objects.create(user=user1, recipe=recipe)

        with self.assertRaises(Exception):
            Save.objects.create(user=user1, recipe=recipe)
        

class ReviewModelTest(TestCase):

    #tests a user cannot review the same recipe mutiple times

    def test_unique_together(self):
        user1 = User.objects.create_user(user='testuser', email='testuser@eg.com', password='testpassword')
        recipe = Recipe.objects.create(title='Test Recipe', quick_description='Test description', content='Test recipe content', ingredients='Test recipe ingredients')
        Review.objects.create(user=user1, recipe=recipe)

        with self.assertRaises(Exception):
            Review.objects.create(user=user1, recipe=recipe)

