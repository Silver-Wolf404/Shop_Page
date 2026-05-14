from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexClassView.as_view(), name='index'),
]