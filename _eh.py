"""PytSite Facebook Plugin Event Handlers.
"""
from pytsite import metatag as _metatag, settings as _settings, auth as _auth, lang as _lang, router as _router

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def router_dispatch():
    """'pytsite.router.dispatch' event handler.
    """
    if _auth.get_current_user().has_permission('facebook.settings.manage'):
        msg = _lang.t('facebook@plugin_setup_required_warning')
        if not _settings.get('facebook.app_id') or not _settings.get('facebook.app_secret'):
            _router.session().add_warning_message(msg)
        else:
            _router.session().get_warning_message(msg)

    _metatag.t_set('fb:app_id', _settings.get('facebook.app_id'))
