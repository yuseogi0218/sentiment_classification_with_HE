from django.contrib import admin
from .models import Diary


class DiaryAdmin(admin.ModelAdmin):
    search_fields = ['author']


admin.site.register(Diary, DiaryAdmin)
