from django.contrib import admin

from .models import ItemCategory, Tsuke


class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ["category"]


class TsukeAdmin(admin.ModelAdmin):
    list_display = ["purchase_date", "amount", "user", "note", "payment_date"]


admin.site.register(ItemCategory, ItemCategoryAdmin)
admin.site.register(Tsuke, TsukeAdmin)
