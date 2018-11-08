from django import forms
from django.forms.models import inlineformset_factory
from .models import (Libro, Autore, Editore, Collana, Genere, SottoGenere,
                    Profilo)


__all__ = ['BootstrapForm']

class BootstrapForm(forms.Form):
    ''' A simple Form to apply bootstrap classes to widgets.
    '''
    def __init__(self, *args, **kwargs):
        super(BootstrapForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            name = field.widget.__class__.__name__.lower()
            if not name.startswith("radio") and not name.startswith("checkbox") and not name == 'fileinput':
                try:
                    classes = field.widget.attrs['class'].split(' ')
                    classes.append('form-control')
                    field.widget.attrs['class'] = ' '.join(set(classes))
                except KeyError:
                    field.widget.attrs['class'] = 'form-control'


class LibroForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['isbn', 'titolo', 'autori', 'descrizione', 'editore',
                  'genere', 'sottogeneri', 'collana', 'profilo_prestito']


class AutoreForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Autore
        fields = ['nome', 'cognome']


class EditoreForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Editore
        fields = ['nome']


class CollanaForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Collana
        fields = ['nome', 'editore']


class GenereForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Genere
        fields = ['nome']


class SottoGenereForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = SottoGenere
        fields = ['nome', 'padre']


class ProfiloForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Profilo
        fields = ['nome', 'cognome', 'codfisc', 'data_nascita', 'telefono',
                  'email']


class ProfiloLibroForm(BootstrapForm, forms.ModelForm):
    libro = forms.ModelChoiceField(
        queryset=Libro.objects.all(),
        required=False
    )

    class Meta:
        model = Profilo
        fields = ['nome', 'cognome', 'codfisc', 'data_nascita', 'telefono',
                  'email']
