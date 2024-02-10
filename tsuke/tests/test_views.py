from django.urls import reverse_lazy

from ..forms import TsukeCreateForm
from ..models import ItemCategory, Tsuke
from .test_account import LoggedInTestCase


class TestTsukeCreateView(LoggedInTestCase):
    """TsukeCreateView用のテストクラス"""

    @classmethod
    def setUpTestData(cls):
        cls.category = ItemCategory.objects.create(category="test_category")

    def test_create_tsuke(self):
        """ツケの登録（正常データの場合）"""
        # ビューのURLを取得
        url = reverse_lazy("tsuke:create")

        # 疑似submit tokenを生成
        self.set_pseudo_token()

        # POSTデータを作成
        data = {
            "amount": 100,
            "category": self.category.id,
            "note": "テストメモ",
            "submit_token": self.SUBMIT_TOKEN
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
