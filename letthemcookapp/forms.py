from django import forms
from .models import Recipe, Review

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'quick_description', 'content', 'ingredients', 'picture']
        widgets = {
            'ingredients': forms.Textarea(attrs={'rows': 10}),
            'content': forms.Textarea(attrs={'rows': 8}),
            'quick_description': forms.Textarea(attrs={'rows': 4}),
        }


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField()
    comment = forms.CharField()
    class Meta:
        model = Review
        fields = ('rating', 'comment')