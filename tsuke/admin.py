from django.contrib import admin
from django.db.models import Sum

from .models import ItemCategory, Tsuke, TsukeTotal


class PaidFilter(admin.SimpleListFilter):
    """清算済みフィルタ"""
    title = "清算"
    parameter_name = "is_paid"

    def lookups(self, request, model_admin):
        return (
            ("paid", "済"),
            ("unpaid", "未"),
        )

    def queryset(self, request, queryset):
        if self.value() == "paid":
            return queryset.filter(is_paid=True)
        if self.value() == "unpaid":
            return queryset.filter(is_paid=False)


class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ["category"]
    change_list_template = "admin/itemcategory_change_list.html"


class TsukeAdmin(admin.ModelAdmin):
    list_display = ["purchase_date", "amount", "user", "note", "is_paid", "payment_date"]
    readonly_fields = [field.name for field in Tsuke._meta.fields]
    list_filter = ["user", "category", PaidFilter]
    change_list_template = "admin/tsuke_change_list.html"  # 一覧画面
    change_form_template = "admin/tsuke_change_form.html"  # 詳細画面

    def has_add_permission(self, request, obj=None) -> bool:
        """ツケは登録ページからしか追加できない"""
        return False
    
    def has_view_permission(self, request, obj=None) -> bool:
        if request.user.is_staff:
            return True  # スタッフは閲覧可能
        return False
    
    def has_delete_permission(self, request, obj=None) -> bool:
        if request.user.is_superuser:
            return True  # スーパーユーザのみ削除可能
        return False
    
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)

        # try:
        #     qs = response.context_data["cl"].get_queryset(request)
        # except (AttributeError, KeyError):
        #     return response
        
        # フィルタ条件を取得
        filters = {
            param: request.GET.getlist(param) for param in request.GET
            if not param.startswith("_")
        }

        response.context_data['filters'] = filters
        return response


class TsukeTotalAdmin(admin.ModelAdmin):
    list_display = ["user"]
    change_list_template = "admin/tsuketotal_change_list.html"

    def has_add_permission(self, *args, **kwargs):
        """ツケの合計は変更できない"""
        return False

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
            user: qs.filter(user=user, is_paid=False).aggregate(**metrics)["total_amount"] or 0
            for user in user_list
        }

        response.context_data["summary"] = total_amount
        return response

admin.site.site_header = "Tsukepp 管理画面"
admin.site.index_title = "メニュー"

admin.site.register(ItemCategory, ItemCategoryAdmin)
admin.site.register(Tsuke, TsukeAdmin)
admin.site.register(TsukeTotal, TsukeTotalAdmin)
