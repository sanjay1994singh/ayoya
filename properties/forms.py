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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            current_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{current_class} form-control".strip()
            if name in {"title", "short_description", "address", "locality", "city", "state", "country"}:
                field.widget.attrs.setdefault("placeholder", field.label)
        for name in ("is_featured", "is_verified"):
            self.fields[name].widget.attrs["class"] = "form-check-input"
        self.fields["amenities"].widget = forms.CheckboxSelectMultiple()
        self.fields["amenities"].widget.attrs["class"] = "amenity-checks"
        self.fields["amenities"].widget.choices = self.fields["amenities"].choices
        self.fields["short_description"].widget.attrs["maxlength"] = "280"
        self.fields["meta_title"].widget.attrs["maxlength"] = "70"
        self.fields["meta_description"].widget.attrs["maxlength"] = "160"

    class Meta:
        model = Property
        exclude = ("owner", "slug", "views_count", "created_at", "updated_at")
        widgets = {
            "short_description": forms.Textarea(attrs={"rows": 3}),
            "address": forms.Textarea(attrs={"rows": 3}),
            "meta_description": forms.Textarea(attrs={"rows": 3}),
        }


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
