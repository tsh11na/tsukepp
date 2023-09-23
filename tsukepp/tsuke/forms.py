from django import forms

from .models import Tsuke


class TsukeCreateForm(forms.ModelForm):
    """ツケの登録"""
    class Meta:
        model = Tsuke
        fields=("amount", "note",)


class TsukePaySelectForm(forms.Form):
    """支払うツケの選択"""
    selected_ids = forms.ModelMultipleChoiceField(
        queryset=None,  # 空のクエリセット（views.pyで選択するため）
        widget=forms.CheckboxSelectMultiple,  # チェックボックスを使って選択
    )


class TsukePayConfirmForm(forms.Form):
    """支払うツケの確認"""
    selected_ids = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
    )
