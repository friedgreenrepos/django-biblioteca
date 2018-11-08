from django.conf import settings

DURATA_PRESTITO = getattr(
    settings,
    'BIBLIOTECA_DURATA_PRESTITO',
    30
)
