from django.contrib import admin
from django.urls import path

from violation.views import HomeView

urlpatterns = [
    path("", HomeView.as_view()),
]
