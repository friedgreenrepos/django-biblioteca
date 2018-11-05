from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    # Libri
    path('elenco-libri/', views.ElencoLibriView.as_view(), name='elenco_libri'),
    path('elenco-libri/<int:pk>/', views.DettaglioLibroView.as_view(), name='dettaglio_libro'),
    path('elenco-libri/aggiungi-libro/', views.AggiungiLibroView.as_view(), name='aggiungi_libro'),
    path('elenco-libri/<int:pk>/modifica-libro', views.ModificaLibroView.as_view(), name='modifica_libro'),
    # Autori
    path('elenco-autori/', views.ElencoAutoriView.as_view(), name='elenco_autori'),
    path('elenco-autori/aggiungi-autore/', views.AggiungiAutoreView.as_view(), name='aggiungi_autore'),
    path('elenco-autori/<int:pk>/modifica-autore', views.ModificaAutoreView.as_view(), name='modifica_autore'),
]
