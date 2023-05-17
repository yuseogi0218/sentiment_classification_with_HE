from django.urls import path

from . import views

app_name = 'diary'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.diary_create, name='diary_create'),
]