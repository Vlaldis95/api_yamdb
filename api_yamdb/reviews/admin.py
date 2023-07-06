from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class TitleAdmin(admin.ModelAdmin):
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
