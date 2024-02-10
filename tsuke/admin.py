from django.contrib import admin
from django.db.models import Sum

from .models import ItemCategory, Tsuke, TsukeTotal


class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ["category"]


class TsukeAdmin(admin.ModelAdmin):
    list_display = ["purchase_date", "amount", "user", "note", "payment_date"]

class TsukeTotalAdmin(admin.ModelAdmin):
    list_display = ["user"]
    change_list_template = "admin/tsuketotal_change_list.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        try:
            qs = response.context_data["cl"].queryset
        except (AttributeError, KeyError):
            return response
        metrics = {
            "total_amount": Sum("amount"),
        }

        # ユーザ一覧を取得
        user_list = [tsuke.user for tsuke in qs]
        # ユーザごとの合計金額を取得
        total_amount = {
            user: qs.filter(user=user).aggregate(**metrics)["total_amount"]
            for user in user_list
        }

        response.context_data["summary"] = total_amount
        return response

admin.site.site_header = "Tsukepp 管理画面"
admin.site.index_title = "メニュー"

admin.site.register(ItemCategory, ItemCategoryAdmin)
admin.site.register(Tsuke, TsukeAdmin)
admin.site.register(TsukeTotal, TsukeTotalAdmin)
