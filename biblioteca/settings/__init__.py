from .base import *

try:
    from local_settings import *
except ImportError as err:
    if 'local_settings' not in str(err):
        raise
