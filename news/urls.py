from . import views
from django.urls import include, path

urlpatterns = [
    path('', views.news_list),
]