from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('elenco-libri/', views.ElencoLibriView.as_view(), name='elenco_libri'),
]
