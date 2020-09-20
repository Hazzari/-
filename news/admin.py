from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import News, Category


@admin.register(News)
class NewAdmin(admin.ModelAdmin):
    ...
    # Отображает заголовки колонок
    list_display = ('id', 'title', 'category', 'created_at', 'is_published', 'get_photo', 'updated_at')
    list_display_links = ('id', 'title',)
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')
    # панельки сверху
    save_on_top = True
    # как выглядит пустое поле
    empty_value_display = '-empty-'


    # Указываем какие поля нужны в редакторе модели
    fields = ('get_photo', 'title', 'category', 'content', 'photo', 'is_published', 'views', 'created_at', 'updated_at')
    # Указываем read only -> те что нельзя редактировать
    readonly_fields = ('get_photo', 'views', 'created_at', 'updated_at')

    # Обработка фотографий.
    # поля которые должны быть представленны внутри.
    def get_photo(self, obj):
        # Возвращает неформатированный код
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')
        # else:
        #     return 'Нет фото'

    # Выводим фото в списке
    get_photo.short_description = 'Миниатюра'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


admin.site.register(Category, CategoryAdmin)

# Управзяет тайтлом и заголовком
admin.site.site_title = 'Управление новостями'
admin.site.site_header = 'Управление новостями'
