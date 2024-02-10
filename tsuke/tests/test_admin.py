from django.urls import reverse_lazy

from ..models import ItemCategory, Tsuke
from .test_account import SuperuserLoggedInTestCase


class TestAdminTsukeTotal(SuperuserLoggedInTestCase):
    """管理サイトのツケ合計表示用のテストクラス"""

    @classmethod
    def setUpTestData(cls):
        cls.category1 = ItemCategory.objects.create(category="飲み物")
        cls.category2 = ItemCategory.objects.create(category="お菓子")

    def test_admin_tsuke_total(self):
        """管理サイトのツケ合計が正しく表示されることを確認"""
        url = reverse_lazy("admin:tsuke_tsuketotal_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # 疑似データを登録
        Tsuke.objects.create(
            amount=123,
            category=self.category1,
            note="お茶",
            is_paid=False,
            user=self.test_user,
        )
        Tsuke.objects.create(
            amount=456,
            category=self.category2,
            note="グミ",
            is_paid=False,
            user=self.test_user,
        )
        Tsuke.objects.create(
            amount=789,
            category=self.category1,
            note="コーヒー",
            is_paid=True,  # 清算済
            user=self.test_user,
        )

        # 未清算のツケのみの合計額が表示されることを確認
        response = self.client.get(url)
        self.assertContains(response, "579")  # 123 + 456
