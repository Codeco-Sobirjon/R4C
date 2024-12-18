from django.contrib import admin
from apps.robots.models import Robot


class RobotAdmin(admin.ModelAdmin):
    list_display = ('serial', 'model', 'version', 'created', 'is_available',)
    list_filter = ('model', 'version', 'is_available')
    search_fields = ('serial', 'model', 'version')
    ordering = ('-created',)
    readonly_fields = ('created',)


admin.site.register(Robot, RobotAdmin)
