from django.contrib import admin
from .models import (Libro, Autore, Genere, SottoGenere, Editore, Collana,
                     Profilo, Segnalazione, Bookmark, Prestito, Documento)


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titolo', 'get_autori_display', 'genere')


@admin.register(Autore)
class AutoreAdmin(admin.ModelAdmin):
    pass


@admin.register(Genere)
class GenereAdmin(admin.ModelAdmin):
    pass


@admin.register(SottoGenere)
class SottoGenereAdmin(admin.ModelAdmin):
    pass


@admin.register(Editore)
class EditoreAdmin(admin.ModelAdmin):
    pass


@admin.register(Collana)
class CollanaAdmin(admin.ModelAdmin):
    pass


@admin.register(Profilo)
class ProfiloAdmin(admin.ModelAdmin):
    pass


@admin.register(Segnalazione)
class SegnalazioneAdmin(admin.ModelAdmin):
    list_display = ('get_tipo_display', 'data')


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('nome', 'user')


@admin.register(Prestito)
class PrestitoAdmin(admin.ModelAdmin):
    list_display = ('profilo', 'libro')


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_upload', 'is_amministrazione')
