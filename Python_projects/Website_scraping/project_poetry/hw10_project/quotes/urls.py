from django.urls import path
from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main, name="root"),
    path("<int:page>", views.main, name="root_paginate"),
    path('add/', views.add_quote, name='add_quote'),
    path('author/create/', views.author_create, name='author_create'),
    path('author/<str:fullname>/', views.author_detail, name='author_detail'),
]
