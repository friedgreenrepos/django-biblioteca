import django_filters
from ..models import (Libro, Autore, Genere, SottoGenere, Editore, Collana,
                      Profilo)


class LibroFilter(django_filters.FilterSet):
    isbn = django_filters.CharFilter(lookup_expr='iexact')
    titolo = django_filters.CharFilter(label='Titolo', lookup_expr='icontains')

    class Meta:
        model = Libro
        fields = ['isbn', 'titolo', 'autori', 'editore',
                  'genere', 'collana', 'stato_prestito']
