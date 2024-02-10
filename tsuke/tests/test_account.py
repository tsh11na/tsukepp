"""テスト用のアカウントやログイン状態を定義するモジュール"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy


class LoggedInTestCase(TestCase):
    """
    ログイン状態を定義するテストケース
    （「動かして学ぶ！Python Django開発入門」p.286より）
    """
    def setUp(self):
        """テストメソッド実行前の事前設定"""
        self.username = "testa"
        self.password = 'xyab2023'
        self.SUBMIT_TOKEN = "test_token"

        self.test_user = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
        )

        self.client.login(
            username=self.username,
            password=self.password
        )

    def set_pseudo_token(self):
        """疑似submit tokenをセッションに格納する"""
        sess = self.client.session
        sess["submit_token"] = self.SUBMIT_TOKEN
        sess.save()


class SuperuserLoggedInTestCase(LoggedInTestCase):
    """管理サイトのログイン状態を定義するクラス"""
    def setUp(self):
        """テストメソッド実行前の事前設定"""
        self.username = "admin"
        self.password = 'admin2023'
        self.SUBMIT_TOKEN = "test_token"

        self.test_user = get_user_model().objects.create_superuser(
            username=self.username,
            email="sample@example.com",
            password=self.password
        )

        self.client.login(
            username=self.username,
            password=self.password
        )

    def set_pseudo_token(self):
        """疑似submit tokenをセッションに格納する"""
        sess = self.client.session
        sess["submit_token"] = self.SUBMIT_TOKEN
        sess.save()


class TestAccount(LoggedInTestCase):
    """アカウント機能のテストクラス"""
    def test_login_ok(self):
        """すでにログイン状態であることの確認"""
        response = self.client.get(
            '/accounts/login/'
        )
        self.assertRedirects(response, reverse_lazy('tsuke:index'))
