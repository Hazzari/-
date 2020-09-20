from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.contrib.auth import login, logout
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy, reverse

import environ
from .utils import UpperMixin
from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactEmailForm

env = environ.Env()


def contact(request):
    if request.method == 'POST':
        form = ContactEmailForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], env('EMAIL_HOST_USER'),
                             [env('EMAIL_TO_USER')],
                             fail_silently=True)  # в Тру чтоб не пугать пользователей при ошибках отправки
            if mail:
                messages.success(request, 'Письмо отправленно')
                return redirect('home')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка валидации')
    else:
        form = ContactEmailForm()
    return render(request, 'news/contact.html', context={'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Для того что бы не авторизовывать после регистрации можно его сразу авторизовать для этого нужно
            user = form.save()
            # присвоить пользователя переменной и передать его функции login
            login(request, user)
            messages.success(request, 'Вы успешно зарегирились')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', context={'form': form})


def user_login(request):
    if request.method == 'POST':
        # нужно присвоить в data=!!!!
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', context={'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


class HomeNews(UpperMixin, ListView):
    paginate_by = 3
    model = News  # Аналог "news = News.objects.all()"
    template_name = "news/home_news_list.html"  #
    context_object_name = 'news'  # Название обьекта куда передаются данные в шаблон

    # queryset = News.objects.select_related('category')

    # extra_context = {'title': ' Главная'}  # Для статичных данных, можно сразу в get_context_data

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    # Только нужный набор обьектов, отфильтрованный
    def get_queryset(self):
        # select_related = Жадный запрос для уменьшения загрузок из SQL
        # Говорим чтоб загрузи сразу и все данные нам понадобятся
        return News.objects.filter(is_published=True).select_related('category')


# def index(request):
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#     }
#     return render(request, template_name='news/app/index.html', context=context)

class NewsByCategory(UpperMixin, ListView):
    paginate_by = 3
    model = News
    template_name = "news/home_news_list.html"  # Отличий нет от индекса
    context_object_name = 'news'  # Название обьекта куда передаются данные в шабло
    allow_empty = False  # не показывать пустые списки ( вернет 404 )

    def get_queryset(self):
        # Номер категории берем из URL ('category/<int:category_id>/')
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))

        return context


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     categories = get_object_or_404(Category, pk=category_id)
#
#     return render(request,
#                   template_name='news/app/category.html',
#                   context={
#                       'news': news,
#                       'categories': categories, })


class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'  # если не указать - в шаблоне будет доступен через object
    # pk_url_kwarg = 'news_id'
    # template_name = 'news/news_detail.html'  # тут используется по умолчанию


#
# def view_news(request, news_id):
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', context={'news_item': news_item})
#

class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    login_url = '/admin/'

    # Если в моделе есть get_absolute_url то произойдет редирект на созданную страницу.
    # Если нет get_absolute_url в моделе можно указать: success_url
    # Использовать reverse вызовет ошибку. использовать лучше reverse_lazy
    # success_url = reverse_lazy('home')

#
# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             print(form.photo)
#             # news = News.objects.create(**form.cleaned_data)  # для обработки формы не связанной с моделью
#             # распаковывываем словарь и присваиваем необходимые значения ключам
#             # аналогично если бы мы писали title=form.cleaned_data['title']
#             news = form.save()  # для обработки формы  связанной с моделью
#             # pprint(news)
#             # pprint(dir(news))
#             return redirect(news)  # отправляем пользователя на созданную новость
#     else:
#         form = NewsForm()
#     return render(request, template_name='news/add_news.html', context={'form': form})
