from django import forms
from logpose.models import Genre, Game, UserProfile, Review
from django.contrib.auth.models import User

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["game", "rating", "body"]
        widgets = {
            'game': forms.Select(attrs={'class': 'form-select'}),
            'rating': forms.RadioSelect(),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write your review here...'
            }),
        }


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta: 
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'profile_image',)


class GameSearchForm(forms.Form):
    game = forms.CharField(required=False)
    genre = forms.CharField(required=False)
    stars = forms.IntegerField(required=False)
    year = forms.IntegerField(required=False)
