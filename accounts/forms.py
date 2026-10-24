from django import forms

from .models import Profile

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio"]
        widgets = {
            "bio": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Tell people a little about yourself…",
                    "maxlength": 160,
                }
            )
        }
        labels = {"bio": "Bio"}
        help_texts = {"bio": "Max 160 characters."}
