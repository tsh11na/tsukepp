from django import forms

from .models import Tsuke


class TsukeCreateForm(forms.ModelForm):
    class Meta:
        model = Tsuke
        fields=("amount", "note",)


class TsukePaySelectForm(forms.Form):
    selected_ids = forms.ModelMultipleChoiceField(
        queryset=None,  # 空のクエリセット（views.pyで選択するため）
        widget=forms.CheckboxSelectMultiple,  # チェックボックスを使って選択
    )


# class TsukePayConfirmForm(forms.Form):
#     tsuke_list = forms.ModelMultipleChoiceField(
#         queryset=None,
#         widget=forms.HiddenInput,
#         required=False  # 必須ではない
#     )
