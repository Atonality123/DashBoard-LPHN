from django.urls import path
from .views import home, finance_data, search_view, dowload_exel

urlpatterns = [
    path("", home, name="home"),
    path("search/", search_view, name="search_view"),
    path("download-excel/", dowload_exel, name="dowload_exel"),
    path("finance_data/<int:member_id>/", finance_data, name="finance_data"),
]
