from django.urls import path

from . import views


app_name = "tsuke"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("create/", views.TsukeCreateView.as_view(), name="create"), # ツケる
    path("history/", views.TsukeHistoryView.as_view(), name="history"),  # ツケ履歴
]
