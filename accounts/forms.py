from allauth.account.forms import LoginForm


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['remember'].initial = True  # 「ログインしたままにする」をデフォルトでONに
