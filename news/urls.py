from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [

    path('test/', test, name='test'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    # path('', index, name='home'),
    # path('category/<int:category_id>/', get_category, name='category'),
    path('', HomeNews.as_view(), name='home'),
    path('category/<int:category_id>/', NewsByCategory.as_view(), name='category'),
    # path('news/<int:news_id>/', view_news, name='view_news'),
    path('news/<int:pk>/', ViewNews.as_view(), name='view_news'),
    # path('news/add-news/', add_news, name='add_news'),
    path('news/add-news/', CreateNews.as_view(), name='add_news'),

]
