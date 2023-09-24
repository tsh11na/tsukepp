from django import forms

from .models import Tsuke


class TsukeCreateForm(forms.ModelForm):
    """ツケの登録"""
    class Meta:
        model = Tsuke
        fields=("amount", "category", "note",)

    def __init__(self, *args, **kwargs):
        for field in self.base_fields.values():
            field.widget.attrs.update({"class":"form-control"})
        request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs.update({'step': '10'})  # REVEIEW: 10円単位しか受け付けなくなるのでナシでもいいかも
        # フィールドに初期値を設定
        # https://omkz.net/djagno-parameter-modelform/
        self.fields['amount'].initial = request.GET.get('amount', 0)
        self.fields['category'].initial = request.GET.get('category_id', 0)

class TsukePaySelectForm(forms.Form):
    """清算するツケの選択"""
    tsuke_list = forms.ModelMultipleChoiceField(
        queryset=Tsuke.objects.none(),  # 空のクエリセット（views.pyで選択するため）
        widget=forms.CheckboxSelectMultiple,  # チェックボックスを使って選択
        
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:  # 「対象のユーザかつ未払い」に絞り込む
            self.fields['tsuke_list'].queryset = Tsuke.objects.filter(user=user, is_paid=False)

class TsukePayConfirmForm(forms.Form):
    """清算するツケの確認"""
    tsuke_list = forms.ModelMultipleChoiceField(
        queryset=Tsuke.objects.none(),
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        tsuke_ids = kwargs.pop('tsuke_ids', None)
        super().__init__(*args, **kwargs)
        if tsuke_ids:  # 対象のIDに絞り込む
            self.fields['tsuke_list'].queryset = Tsuke.objects.filter(id__in=tsuke_ids)
