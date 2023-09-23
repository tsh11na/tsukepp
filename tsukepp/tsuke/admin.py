from django.contrib import admin

from .models import Tsuke, ItemCategory


class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ["category"]


class TsukeAdmin(admin.ModelAdmin):
    list_display = ["purchase_datetime", "amount", "user", "note"]


admin.site.register(ItemCategory, ItemCategoryAdmin)
admin.site.register(Tsuke, TsukeAdmin)
