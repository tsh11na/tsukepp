from django.contrib import admin

from .models import Tsuke

class TsukeAdmin(admin.ModelAdmin):
    list_display = ["purchase_datetime", "amount", "user", "note"]

admin.site.register(Tsuke, TsukeAdmin)
