from django.urls import path
from . import views

urlpatterns = [
    path('', views.commodity, name='commodity'),
    path('detail/<int:id>/', views.detail, name='detail'),
]