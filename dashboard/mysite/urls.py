from django.urls import path
from .views import home, finance_data

urlpatterns = [
    path("", home, name="home"),
    path("finance_data/<int:member_id>/", finance_data, name="finance_data"),
]
