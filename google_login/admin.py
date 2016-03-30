from django.contrib import admin

from google_login.models import GoogleProfile


class GoogleProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'google_id', 'access_token', 'profile_data')
    list_filter = ('user__first_name', 'user__last_name', 'user__email', 'google_id')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'google_id')


admin.site.register(GoogleProfile, GoogleProfileAdmin)
