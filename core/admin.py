from django.contrib import admin
from .models import (Libro, Autore, Genere, SottoGenere, Editore, Collana,
                     RichiestaPrestito, Prestito)


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titolo', 'get_autori_display', 'genere')
    list_filter = ('genere', 'disponibile', 'data_restituzione')


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


@admin.register(RichiestaPrestito)
class RichiestaPrestitoAdmin(admin.ModelAdmin):
    pass


@admin.register(Prestito)
class PrestitoAdmin(admin.ModelAdmin):
    pass
