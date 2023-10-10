from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from .forms import CustomSignupForm


@override_settings(TSUKEPP_ACTIVATION_KEY='correct_activation_key')
class ActivationKeyTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'testuser@example.com',
        }

    def test_correct_activation_key(self):
        """正しいアクティベーションキーを送信した場合フォームが有効になることを確認"""
        self.user_data["activation_key"] = 'correct_activation_key'
        form = CustomSignupForm(data=self.user_data, activation_key='correct_activation_key')
        self.assertTrue(form.is_valid())

    def test_incorrect_activation_key(self):
        """不正なアクティベーションキーを送信した場合フォームが無効になることを確認"""
        self.user_data['activation_key'] = 'incorrect_activation_key'  # 間違ったキーを指定
        form = CustomSignupForm(data=self.user_data, activation_key='correct_activation_key')
        self.assertFalse(form.is_valid())

    def test_without_activation_key(self):
        """アクティベーションキーをが設定されていない場合フォームが有効になることを確認"""
        self.user_data['activation_key'] = ''
        form = CustomSignupForm(data=self.user_data, activation_key='')  # アクティベーションキー未設定
        self.assertTrue(form.is_valid())
