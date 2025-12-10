from django.urls import path
from . import views
from .views import calculator_view


urlpatterns=[
    path('',views.home,name="home"),
    path("calculator/", views.calculator_view, name="calculator"),
]