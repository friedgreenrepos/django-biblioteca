from django.db.models import Q
import django_filters
from ..models import (Libro, Autore, Genere, SottoGenere, Editore, Collana,
                      Profilo)


class LibroFilter(django_filters.FilterSet):
    isbn = django_filters.CharFilter(lookup_expr='iexact')
    titolo = django_filters.CharFilter(label='Titolo', lookup_expr='icontains')

    class Meta:
        model = Libro
        fields = ['isbn', 'titolo', 'autori', 'editore',
                  'genere', 'collana']


# class LibroPrestitoFilter(django_filters.FilterSet):
#     PRESTITO_CHOICES = (
#         ('PN', 'Pendente'),
#         ('PR', 'In prestito'),
#     )
#     stato_prestito = django_filters.ChoiceFilter(choices=PRESTITO_CHOICES, label= 'Stato prestito')
#     isbn = django_filters.CharFilter(lookup_expr='iexact')
#     titolo = django_filters.CharFilter(label='Titolo Libro', lookup_expr='icontains')
#
#     class Meta:
#         model = Libro
#         fields = ['profilo_prestito']
