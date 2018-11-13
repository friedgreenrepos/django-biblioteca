from django.conf import settings

GIORNI_PRESTITO = getattr(
    settings,
    'BIBLIOTECA_GIORNI_PRESTITO',
    30
)

MAX_LIBRI_INPRESTITO = getattr(
    settings,
    'BIBLIOTECA_MAX_LIBRI_INPRESTITO',
    4
)

GIORNI_SOSPENSIONE = getattr(
    settings,
    'BIBLIOTECA_GIORNI_SOSPENSIONE',
    10
)

MAXKB_DOCUMENTO = getattr(
    settings,
    'BIBLIOTECA_MAXKB_DOCUMENTO',
    50
)
