from django.contrib import admin
from .models import Nyaaan


class NyaaanAdmin(admin.ModelAdmin):
    list_display = ('short_text', 'echo', 'slug', 'user', 'created_at')


admin.site.register(Nyaaan, NyaaanAdmin)
