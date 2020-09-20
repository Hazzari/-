from django.db import models
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length=50, verbose_name='Наименование', )
    content = models.TextField(blank=True, verbose_name='Текст новости')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата публикации ')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    # Валидируем. чтобы файл был Image, upload_to= указывает куда сохранять, разбивая их по дате
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Фото')
    is_published = models.BooleanField(default=True, verbose_name='статус')

    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse(viewname='view_news', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']


class Category(models.Model):
    title = models.CharField(
        max_length=150, db_index=True, verbose_name='Наименование категории')

    def __str__(self):
        return f'{self.title}'

    # Джанго сам выстроит ссылку
    def get_absolute_url(self):
        return reverse(viewname='category', kwargs={'category_id': self.pk})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['title']
