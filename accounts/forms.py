from allauth.account.forms import LoginForm, SignupForm
from django import forms

from tsukepp.settings_common import TSUKEPP_ACTIVATION_KEY

# ここで書いたフォームは settings.ACCOUNT_FORMS で有効化


class CustomSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        self.correct_activation_key = kwargs.pop('activation_key', TSUKEPP_ACTIVATION_KEY)
        super().__init__(*args, **kwargs)

    activation_key = forms.CharField(
        max_length=100,
        required=False,
        label="アクティベーションキー",
        widget=forms.PasswordInput(attrs={'placeholder': "アクティベーションキー"}),
        help_text="管理者から提供されたキーがあれば入力してください。"
    )

    def clean_activation_key(self):
        activation_key = self.cleaned_data.get('activation_key')
        correct_activation_key = self.correct_activation_key  # 正しいアクティベーションキーを設定

        if activation_key and activation_key != correct_activation_key:
            raise forms.ValidationError('アクティベーションキーが正しくありません。')

        return activation_key


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['remember'].initial = True  # 「ログインしたままにする」をデフォルトでONに
