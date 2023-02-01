from django.urls import path
from user import views

urlpatterns = [
    path("test/", views.index, name='index')
]