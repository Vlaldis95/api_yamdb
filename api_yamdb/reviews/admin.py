from django.contrib import admin

from .models import Category, Title, Genre


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'rating', 'description')
    search_fields = ('name', 'year', 'description', 'rating')
    list_filter = ('rating', 'year')
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
