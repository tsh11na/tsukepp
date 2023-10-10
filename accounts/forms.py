from allauth.account.forms import LoginForm, SignupForm
from django import forms

# ここで書いたフォームは settings.ACCOUNT_FORMS で有効化


class CustomSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        try:
            from tsukepp.settings_common import TSUKEPP_ACTIVATION_KEY
            self.correct_activation_key = kwargs.pop('activation_key', TSUKEPP_ACTIVATION_KEY)
        except ImportError:
            self.correct_activation_key = ''
        super().__init__(*args, **kwargs)

    activation_key = forms.CharField(
        max_length=100,
        required=False,
        label="アクティベーションキー（オプション）",
        widget=forms.PasswordInput(attrs={'placeholder': "アクティベーションキー"}),
        help_text="アカウント作成に必要なキーです。管理者から提供されている場合は入力してください。"
    )

    def clean_activation_key(self):
        activation_key = self.cleaned_data['activation_key']

        if activation_key == self.correct_activation_key:
            return activation_key

        raise forms.ValidationError('アクティベーションキーが正しくありません。')


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['remember'].initial = True  # 「ログインしたままにする」をデフォルトでONに
