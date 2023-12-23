from django.contrib import admin
from .models import Member


class MemberAdmin(admin.ModelAdmin):
    list_display = ["projectName", "agency", "status"]


admin.site.register(Member, MemberAdmin)
