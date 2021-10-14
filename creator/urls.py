from django.urls import path

from creator import views


app_name = 'creator'

urlpatterns = [
    path('', views.index),
    path('<str:keyword>', views.suprize_landing),
]
