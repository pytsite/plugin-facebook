"""PytSite Facebook Plugin
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import plugman as _plugman

if _plugman.is_installed(__name__):
    # Public API
    from ._api import get_app_id, get_app_secret
    from . import _error as error, _session as session, _widget as widget


def plugin_load():
    from pytsite import lang, router
    from plugins import permissions, settings, assetman
    from . import _eh, _settings_form, _controllers

    # Resources
    lang.register_package(__name__)

    assetman.register_package(__name__)
    assetman.t_copy_static(__name__)

    # Lang globals
    lang.register_global('facebook_admin_settings_url', lambda language, args: settings.form_url('facebook'))

    # Routes
    router.handle(_controllers.Authorize, '/facebook/authorize', 'facebook@authorize')

    # Permissions
    permissions.define_permission('facebook.settings.manage', 'facebook@manage_facebook_settings', 'app')

    # Settings
    settings.define('facebook', _settings_form.Form, 'facebook@facebook', 'fa fa-facebook', 'facebook.settings.manage')

    # Event handlers
    router.on_dispatch(_eh.router_dispatch)
