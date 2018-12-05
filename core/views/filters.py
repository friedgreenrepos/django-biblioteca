from datetime import date
from django.db.models import Q
from django.forms import CheckboxInput
import django_filters
from dal import autocomplete
from ..models import (Libro, Autore, Genere, SottoGenere, Editore, Collana,
                      Profilo, Prestito, Documento)


class LibroFilter(django_filters.FilterSet):
    # isbn = django_filters.CharFilter(lookup_expr='iexact')
    titolo_isbn = django_filters.CharFilter(
        label="Titolo/ISBN",
        lookup_expr='icontains',
        method="cerca_titolo_isbn"
    )
    autori = django_filters.ModelMultipleChoiceFilter(
        label='Autori',
        field_name='autori',
        queryset= Autore.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='autore_dal',),
    )
    editore = django_filters.ModelChoiceFilter(
        label='Editore',
        field_name='editore',
        required=False,
        queryset= Editore.objects.all(),
        widget=autocomplete.ModelSelect2(url='editore_dal',),
    )
    collana = django_filters.ModelChoiceFilter(
        label='Collana',
        field_name='collana',
        queryset= Collana.objects.all(),
        widget=autocomplete.ModelSelect2(url='collana_dal', forward=('editore',)),
    )
    genere = django_filters.ModelChoiceFilter(
        label='Genere',
        field_name='genere',
        queryset= Genere.objects.all(),
        widget=autocomplete.ModelSelect2(url='genere_dal',),
    )

    class Meta:
        model = Libro
        fields = ['titolo_isbn', 'autori', 'editore',
                  'genere', 'collana']

    def cerca_titolo_isbn(self, queryset, name, value):
        return queryset.filter(Q(titolo__icontains=value) | Q(isbn__icontains=value))


class PrestitoFilter(django_filters.FilterSet):
    stato = django_filters.ChoiceFilter(
        choices=Prestito.STATI_PRESTITO,
        label="Stato prestito"
    )
    libro = django_filters.ModelChoiceFilter(
        label="Libro",
        queryset=Libro.objects.all()
    )
    scaduto = django_filters.BooleanFilter(
        label='Scaduto',
        field_name='data_scadenza',
        widget=CheckboxInput(),
        method="cerca_prestito_scaduto"
    )

    class Meta:
        model = Prestito
        fields = ['profilo']

    def cerca_prestito_scaduto(self, queryset, name, value):
        if value:
            return queryset.filter(data_scadenza__lte=date.today())
        else:
            return queryset


class DocumentoFilter(django_filters.FilterSet):
    is_amministrazione = django_filters.BooleanFilter(
        label='Amministrazione',
        field_name='is_amministrazione',
        widget=CheckboxInput(),
        method='cerca_documento_amministrazione'
    )
    nome = django_filters.CharFilter(
        label="Nome file",
        lookup_expr='icontains',
    )

    class Meta:
        model = Documento
        fields = ['is_amministrazione', 'nome', 'user', 'data_upload']

    def cerca_documento_amministrazione(self, queryset, name, value):
        if value:
            return queryset.filter(is_amministrazione=True)
        else:
            return queryset
