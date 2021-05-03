from django.urls import path
from . import views

app_name = 'pan_tilt'

urlpatterns = [
    path("", views.index, name="index"),
    path("json/", views.json, name="json"),
]