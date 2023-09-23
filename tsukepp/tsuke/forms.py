from django import forms

from .models import Tsuke


class TsukeCreateForm(forms.ModelForm):
    class Meta:
        model = Tsuke
        fields=("amount", "note",)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
