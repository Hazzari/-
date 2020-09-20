"""

Решаем проблему дублирования запроса sql категорий на каждой странице если работаем с функциями view

"""

from django import template
from django.db.models import Count, F

from news.models import Category

# Регистрация происходит так (согласно документации)
register = template.Library()


# создаем для того что бы не дублировать запросы во вьюхах
@register.simple_tag(name='get_list_categories')
def get_categories():
    return Category.objects.all()


@register.inclusion_tag(filename='news/app/list_categories.html')
def show_categories(arg1='Для', arg2='примера'):
    # categories = Category.objects.all()
    # categories = Category.objects.annotate(count_category=Count('news')).filter(count_category__gt=0)
    # Подсчитывает количество опубликованных статей и выводит в категории со значением больше 0
    categories = Category.objects.annotate(count_category=Count('news', filter=F('news__is_published'))).filter(
        count_category__gt=0)

    return {'categories': categories,
            'arg1': arg1,
            'arg2': arg2}
