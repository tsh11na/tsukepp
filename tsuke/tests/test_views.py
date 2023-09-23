from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from ..models import Tsuke, ItemCategory
from ..forms import TsukeCreateForm


class LoggedInTestCase(TestCase):
    """
    各テストクラスで共通の事前準備処理をオーバーライドした
    独自TestCaseクラス
    （「動かして学ぶ！Python Django開発入門」p.286より）
    """
    def setUp(self):
        """テストメソッド実行前の事前設定"""
        self.username = "testa"
        self.password = 'xyab2023'

        self.test_user = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
        )

        self.client.login(
            username=self.username,
            password=self.password
        )


class TestAccount(LoggedInTestCase):
    """アカウント機能のテストクラス"""
    def test_login_ok(self):
        """すでにログイン状態であることの確認"""
        response = self.client.get(
            '/accounts/login/'
        )
        self.assertRedirects(response, reverse_lazy('tsuke:index'))


class TestTsukeCreateView(LoggedInTestCase):
    """TsukeCreateView用のテストクラス"""

    @classmethod
    def setUpTestData(cls):
        cls.category = ItemCategory.objects.create(category="test_category")

    def test_create_tsuke(self):
        """ツケの登録（正常データの場合）"""
        # ビューのURLを取得
        url = reverse_lazy("tsuke:create")

        # POSTデータを作成
        data = {
            "amount": 100,
            "category": self.category.id,
            "note": "テストメモ",
        }
        form = TsukeCreateForm(data)
        self.assertTrue(form.is_valid())

        # フォームを送信
        response = self.client.post(url, data)

        # フォームが正しく処理され、リダイレクトされるかを確認
        self.assertEqual(response.status_code, 302)  # リダイレクトのHTTPステータスコード

        # ツケがデータベースに正しく保存されたかを確認
        self.assertEqual(Tsuke.objects.count(), 1)
        tsuke = Tsuke.objects.first()
        self.assertEqual(tsuke.amount, data["amount"])
        self.assertEqual(tsuke.category.id, data["category"])
        self.assertEqual(tsuke.note, data["note"])

    def test_create_tsuke_invalid_form(self):
        """ツケの登録（不正データの場合）"""
        url = reverse_lazy("tsuke:create")
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)  # エラーが表示されたページのHTTPステータスコード
        self.assertFormError(response, "form", "amount", "このフィールドは必須です。")
