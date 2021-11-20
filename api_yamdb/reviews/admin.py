from django.contrib import admin

from .models import Category, Comments, Genre, Review, Title


class TitleAdmin(admin.ModelAdmin):
    """Class that configures the display of Title  model. """
    list_display = ('pk', 'year', 'description', 'category', 'name')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    """Class that configures the display of Review  model. """
    list_display = ('pk', 'author', 'title', 'text')
    search_fields = ('author',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class CommentsAdmin(admin.ModelAdmin):
    """Class that configures the display of Comments  model. """
    list_display = ('pk', 'author', 'review', 'text')
    search_fields = ('author',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Genre)
admin.site.register(Category)
