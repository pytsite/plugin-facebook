"""PytSite Facebook Plugin.
"""
# Public API
from ._session import AuthSession, Session

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import lang, assetman, content_export, router, tpl, comments, events, permissions, settings
    from . import _eh, _settings_form, _content_export, _comments

    # Resources
    lang.register_package(__name__, alias='facebook')
    assetman.register_package(__name__, alias='facebook')
    tpl.register_package(__name__, alias='facebook')

    # Lang globals
    lang.register_global('facebook_admin_settings_url', lambda: settings.form_url('facebook'))

    # Routes
    router.add_rule('/facebook/authorize', 'facebook@authorize', __name__ + '@authorize')

    # Content export driver
    content_export.register_driver(_content_export.Driver())

    # Comments driver
    comments.register_driver(_comments.Driver())

    # Permissions
    permissions.define_permission('facebook.settings.manage', 'facebook@manage_facebook_settings', 'app')

    # Settings
    settings.define('facebook', _settings_form.Form, 'facebook@facebook', 'fa fa-facebook', 'facebook.settings.manage')

    # Event handlers
    events.listen('pytsite.router.dispatch', _eh.router_dispatch)


_init()
