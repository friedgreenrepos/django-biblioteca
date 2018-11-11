from django.db.models import Q
import django_filters
from ..models import (Libro, Autore, Genere, SottoGenere, Editore, Collana,
                      Profilo, Prestito)


class LibroFilter(django_filters.FilterSet):
    isbn = django_filters.CharFilter(lookup_expr='iexact')
    titolo = django_filters.CharFilter(label='Titolo', lookup_expr='icontains')

    class Meta:
        model = Libro
        fields = ['isbn', 'titolo', 'autori', 'editore',
                  'genere', 'collana']


class PrestitoFilter(django_filters.FilterSet):
    stato = django_filters.ChoiceFilter(
        choices=Prestito.STATI_PRESTITO,
        label='Stato prestito'
    )
    libro = django_filters.ModelChoiceFilter(
        label='Libro',
        queryset=Libro.objects.all()
    )

    class Meta:
        model = Prestito
        fields = ['profilo']
