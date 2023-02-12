from django.contrib import admin
from .models import Post, Group


class PostAdmin(admin.ModelAdmin):
    # Создания таблицы Post для управления в админке
    list_display = ('pk', 'text', 'pub_date', 'author', 'group')
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)
# Передача определённой ранее структуры в админку


class GroupAdmin(admin.ModelAdmin):
    # Создания таблицы Group для управления в админке
    list_display = ('pk', 'title', 'slug', 'description')


admin.site.register(Group, GroupAdmin)
# Передача определённой ранее структуры в админку
