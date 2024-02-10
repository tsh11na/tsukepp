from django.contrib import admin

from .models import ItemCategory, Tsuke


class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ["category"]


class TsukeAdmin(admin.ModelAdmin):
    list_display = ["purchase_date", "amount", "user", "note", "payment_date"]


admin.site.site_header = "Tsukepp 管理画面"
admin.site.index_title = "メニュー"

admin.site.register(ItemCategory, ItemCategoryAdmin)
admin.site.register(Tsuke, TsukeAdmin)
