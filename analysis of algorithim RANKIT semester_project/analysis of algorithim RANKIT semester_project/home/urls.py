from django.contrib import admin
from django.urls import path,include
from home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('search_result', views.search_result, name='search_result'),
    path('view_page', views.view_page, name='view_page')
]
