from django import forms

from .models import Inquiry, Property, Review


class PropertySearchForm(forms.Form):
    q = forms.CharField(required=False, label="Search")
    purpose = forms.ChoiceField(required=False, choices=[("", "Any purpose")] + list(Property.Purpose.choices))
    property_type = forms.ChoiceField(required=False, choices=[("", "Any type")] + list(Property.Type.choices))
    city = forms.CharField(required=False)
    min_price = forms.DecimalField(required=False, min_value=0)
    max_price = forms.DecimalField(required=False, min_value=0)
    bedrooms = forms.IntegerField(required=False, min_value=0)


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ("owner", "slug", "views_count", "created_at", "updated_at")


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ("name", "email", "phone", "message")
        widgets = {"message": forms.Textarea(attrs={"rows": 4})}


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("rating", "comment")
        widgets = {"comment": forms.Textarea(attrs={"rows": 4})}
