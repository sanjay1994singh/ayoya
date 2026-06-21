from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    accepts_terms = forms.BooleanField(required=True, label="I agree to the terms")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "user_type",
            "city",
            "preferred_location",
            "accepts_terms",
            "password1",
            "password2",
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "alternate_phone",
            "profile_image",
            "bio",
            "company_name",
            "license_number",
            "website",
            "address",
            "city",
            "state",
            "country",
            "postal_code",
            "preferred_location",
            "min_budget",
            "max_budget",
        )
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }
