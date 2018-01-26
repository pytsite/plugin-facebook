"""PytSite Facebook Plugin API Functions.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import reg as _reg
from . import _error


def get_app_id() -> str:
    """Get application's ID.
    """
    app_id = _reg.get('facebook.app_id') or _reg.get('facebook.app_id')

    if not app_id:
        raise _error.AppIdNotSet("Configuration parameter 'facebook.app_id' is not set")

    return app_id


def get_app_secret() -> str:
    """Get application's secret key.
    """
    app_secret = _reg.get('facebook.app_secret') or _reg.get('facebook.app_secret')

    if not app_secret:
        raise _error.AppSecretNotSet("Configuration parameter 'facebook.app_secret' is not set")

    return app_secret
