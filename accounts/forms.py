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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "username": "Choose username",
            "first_name": "First name",
            "last_name": "Last name",
            "email": "Email address",
            "phone": "Phone number",
            "city": "City",
            "preferred_location": "Preferred location",
            "password1": "Password",
            "password2": "Confirm password",
        }
        for name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            if name in placeholders:
                field.widget.attrs["placeholder"] = placeholders[name]
        self.fields["accepts_terms"].widget.attrs["class"] = "form-check-input"


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

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
