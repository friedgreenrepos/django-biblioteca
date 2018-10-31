from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('elenco-libri/', views.ElencoLibriView.as_view(), name='elenco_libri'),
    path('elenco-libri/<int:pk>/', views.DettaglioLibroView.as_view(), name='dettaglio_libro'),
]
