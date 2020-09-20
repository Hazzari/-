from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

# from .models import Category
from .models import News


# forms.Form - не связанное с моделью
# forms.ModelForm - связанное с моделью


# class NewsForm(forms.Form):
#
#     title = forms.CharField(max_length=50, label='Название', widget=forms.TextInput(attrs={'class': 'form-control'}))
#     content = forms.CharField(label='Текст новости',
#                               required=False,  # Не обязательный
#                               widget=forms.Textarea(attrs={
#                                   'class': 'form-control',  # Нужные атрибуты формы передаем через словарь
#                                   'rows': 5}))
#     is_published = forms.BooleanField(label='Статус публикации', initial=True)
#     category = forms.ModelChoiceField(Category.objects.all(),
#                                       label='Категория',
#                                       empty_label='Выберите категорию',
#                                       widget=forms.Select(
#                                           attrs={'class': 'form-control'}))


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        # fields = '__all__'  # все поля, но не рекомендуется

        fields = ['title', 'content', 'is_published', 'photo', 'category']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинатья с цифры')

        return title


# Регистрация
class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        """Убираем автофокус"""
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)

    # С регистрацией не получилось через META назначить attrs полям, по этому переопределили поля в моделе
    username = forms.CharField(label='Имя пользователя', help_text='Максимум 150 символов',
                               widget=forms.TextInput(attrs={'class': 'form-control', }))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='e-mail',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control', }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # Мета не нужен в AuthenticationForm


class ContactEmailForm(forms.Form):
    subject = forms.CharField(label='Тема письма', widget=forms.TextInput(attrs={'class': 'form-control', }))
    content = forms.CharField(label='Текст письма',
                              widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    # email = forms.EmailField()
    # name = forms.CharField(max_length=25)
