from django.urls import path

from . import views

app_name = "tsuke"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("create/", views.TsukeCreateView.as_view(), name="create"), # ツケる
    path("pay/select/", views.tsuke_pay_select, name="pay_select"),  # 清算する（選択）
    path("pay/confirm/", views.TsukePayConfirmView.as_view(), name="pay_confirm"),  # 清算する（確認）
    path("settle/", views.settle, name="settle"),  # 決済
    path("history/", views.TsukeHistoryView.as_view(), name="history"),  # ツケ履歴
]
