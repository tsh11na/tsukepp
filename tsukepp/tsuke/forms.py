from django import forms

from .models import Tsuke
from .custom import CustomModelChoiceField

class TsukeCreateForm(forms.ModelForm):
    """ツケの登録"""
    class Meta:
        model = Tsuke
        fields=("amount", "note",)


class TsukePaySelectForm(forms.Form):
    """支払うツケの選択"""
    tsuke_list = CustomModelChoiceField(
        queryset=Tsuke.objects.none(),  # 空のクエリセット（views.pyで選択するため）
        widget=forms.CheckboxSelectMultiple,  # チェックボックスを使って選択
        
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:  # 「対象のユーザかつ未払い」に絞り込む
            self.fields['tsuke_list'].queryset = Tsuke.objects.filter(user=user, is_paid=False)

class TsukePayConfirmForm(forms.Form):
    """支払うツケの確認"""
    tsuke_list = CustomModelChoiceField(
        queryset=Tsuke.objects.none(),
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        tsuke_ids = kwargs.pop('tsuke_ids', None)
        super().__init__(*args, **kwargs)
        if tsuke_ids:  # 対象のIDに絞り込む
            self.fields['tsuke_list'].queryset = Tsuke.objects.filter(id__in=tsuke_ids)
