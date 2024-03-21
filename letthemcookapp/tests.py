from django.test import TestCase
from django.contrib.auth.models import User
from .models import Recipe, Review, Save
from django.urls import reverse

# MODEL TESTS

class RecipeModelTest(TestCase):

    #tests 'average_rating' field of recipe is updated

    def test_update_average(self):
        user1 = User.objects.create_user(username='testuser', email='testuser@eg.com', password='testpassword')
        user2 = User.objects.create_user(username='testuser2', email='testuser2@eg.com', password='testpassword2')
        user3 = User.objects.create_user(username='testuser3', email='testuser3@eg.com', password='testpassword3')
        recipe = Recipe.objects.create(title='Test Recipe', quick_description='Test description', content='Test recipe content', ingredients='Test recipe ingredients', user=user1)
        review1 = Review.objects.create(recipe=recipe, user=user2, rating=5, comment='very good')
        review2 = Review.objects.create(recipe=recipe, user=user3, rating=4, comment='good')

        recipe.refresh_from_db()
        self.assertEqual(recipe.average_rating, 4.5)

    #test 'saves' field of recipe is updated when recipe is saved

    def test_update_saves(self):
        user1 = User.objects.create_user(username='testuser', email='testuser@eg.com', password='testpassword')
        user2 = User.objects.create_user(username='testuser2', email='testuser2@eg.com', password='testpassword2')
        user3 = User.objects.create_user(username='testuser3', email='testuser3@eg.com', password='testpassword3')
        recipe = Recipe.objects.create(title='Test Recipe', quick_description='Test description', content='Test recipe content', ingredients='Test recipe ingredients', user=user1)
        save1 = Save.objects.create(user=user2, recipe=recipe)
        save2 = Save.objects.create(user=user3, recipe=recipe)

        recipe.update_saves()
        self.assertEqual(recipe.saves, 2)

class SaveModelTest(TestCase):

    #tests a user cannot save the same recipe mutiple times

    def test_unique_together(self):
        user1 = User.objects.create_user(username='testuser', email='testuser@eg.com', password='testpassword')
        user2 = User.objects.create_user(username='testuser2', email='testuser2@eg.com', password='testpassword2')
        recipe = Recipe.objects.create(title='Test Recipe', quick_description='Test description', content='Test recipe content', ingredients='Test recipe ingredients', user= user1)
        Save.objects.create(user=user2, recipe=recipe)

        with self.assertRaises(Exception):
            Save.objects.create(user=user2, recipe=recipe)
        

class ReviewModelTest(TestCase):

    #tests a user cannot review the same recipe mutiple times

    def test_unique_together(self):
        user1 = User.objects.create_user(username='testuser', email='testuser@eg.com', password='testpassword')
        user2 = User.objects.create_user(username='testuser2', email='testuser2@eg.com', password='testpassword2')
        recipe = Recipe.objects.create(title='Test Recipe', quick_description='Test description', content='Test recipe content', ingredients='Test recipe ingredients', user=user1)
        Review.objects.create(user=user2, recipe=recipe, rating=5, comment='amazing')

        with self.assertRaises(Exception):
            Review.objects.create(user=user2, recipe=recipe, rating=2, comment='good')


#VIEWS TESTS
