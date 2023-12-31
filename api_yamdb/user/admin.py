from django.contrib import admin
from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ('pk', 'username', 'email', 'first_name', 'last_name',
                    'bio', 'role')
    empty_value_display = 'значение отсутствует'
    list_editable = ('role',)
    list_filter = ('username',)
    list_per_page = 10
    search_fields = ('username', 'role')
