"""PytSite Facebook Plugin Event Handlers.
"""
from pytsite import metatag as _metatag, auth as _auth, lang as _lang, router as _router
from . import _api, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def router_dispatch():
    """'pytsite.router.dispatch' event handler.
    """
    msg = _lang.t('facebook@plugin_setup_required_warning')
    has_perm = _auth.get_current_user().has_permission('facebook.settings.manage')

    try:
        app_id = _api.get_app_id()
        _metatag.t_set('fb:app_id', app_id)

        if has_perm:
            _router.session().get_warning_message(msg)

    except (_error.AppIdNotSet, _error.AppSecretNotSet):
        if has_perm:
            _router.session().add_warning_message(msg)
