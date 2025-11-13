# accounts/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile
from django.contrib.auth.models import User

User = get_user_model()

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username"]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Username"}),
        }
        

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["display_name", "bio", "avatar"]
        widgets = {
            "display_name": forms.TextInput(attrs={"placeholder": "Enter your name"}),
            "bio": forms.Textarea(attrs={"rows": 4, "placeholder": "Tell us about yourself..."}),
            "avatar": forms.FileInput(attrs={"accept": "image/*"}),
        }

class SecurityForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.setdefault("class", "input")
