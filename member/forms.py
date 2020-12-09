from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile


class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter password',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter password again..',
    }))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your email'
            })
        }


class CreateProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'about_me', 'location',
                  'favourite_anime', 'favourite_genres']
        widgets = {
            'about_me': forms.Textarea(attrs={
                'class': 'form-control w-100'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'favourite_anime': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            })

        }

    @property
    def checked_favourite_genres(self):
        return set(str(i) for i in self.instance.favourite_genres)


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
