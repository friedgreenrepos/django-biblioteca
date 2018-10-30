from django.urls import path
from . import views

urlpatterns = [
    path('elenco-libri/', views.ElencoLibriView.as_view(), name='elenco_libri'),
]
