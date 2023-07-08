from django.contrib import admin

from .models import (Category, Comment,
                     Genre, Review,
                     Title, User, TitleGenre)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Класс настройки раздела пользователей."""

    list_display = ('pk', 'username', 'email', 'first_name', 'last_name',
                    'bio', 'role')
    empty_value_display = 'значение отсутствует'
    list_editable = ('role',)
    list_filter = ('username',)
    list_per_page = 10
    search_fields = ('username', 'role')


class TitleGenreInLine(admin.TabularInline):
    model = TitleGenre


class TitleAdmin(admin.ModelAdmin):
    inlines = [TitleGenreInLine]
    list_display = ('pk', 'name', 'year', 'description')
    search_fields = ('name', 'year', 'description')
    list_filter = ('year',)
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'review')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'pub_date', 'author', 'score')
    search_fields = ('title',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
