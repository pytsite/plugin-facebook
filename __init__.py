"""PytSite Facebook Plugin.
"""
# Public API
from ._api import get_app_id, get_app_secret
from . import _error as error, _session as session, _widget as widget

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import lang, assetman, router, events, permissions, settings
    from . import _eh, _settings_form

    # Resources
    lang.register_package(__name__, alias='facebook')
    assetman.register_package(__name__, alias='facebook')

    # Lang globals
    lang.register_global('facebook_admin_settings_url', lambda language, args: settings.form_url('facebook'))

    # Routes
    router.add_rule('/facebook/authorize', 'plugins.facebook@authorize', 'facebook@authorize')

    # Permissions
    permissions.define_permission('facebook.settings.manage', 'facebook@manage_facebook_settings', 'app')

    # Settings
    settings.define('facebook', _settings_form.Form, 'facebook@facebook', 'fa fa-facebook', 'facebook.settings.manage')

    # Event handlers
    events.listen('pytsite.router.dispatch', _eh.router_dispatch)


_init()
