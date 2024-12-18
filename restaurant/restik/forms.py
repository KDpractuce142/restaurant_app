from django import forms
from .models import User, Food
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
class FoodCreationForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'weight', 'description', 'price', 'image', 'category']


