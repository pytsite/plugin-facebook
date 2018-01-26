"""PytSite Facebook Plugin Settings Form.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import lang as _lang, validation as _validation
from plugins import widget as _widget, settings as _settings
from . import _api, _error


class Form(_settings.Form):
    def _on_setup_widgets(self):
        app_id = ''
        app_secret = ''
        try:
            app_id = _api.get_app_id()
            app_secret = _api.get_app_secret()
        except (_error.AppIdNotSet, _error.AppSecretNotSet):
            pass

        self.add_widget(_widget.input.Text(
            uid='setting_app_id',
            weight=10,
            label=_lang.t('facebook@app_id'),
            required=True,
            help=_lang.t('facebook@app_id_setup_help'),
            rules=_validation.rule.Integer(),
            default=app_id,
        ))

        self.add_widget(_widget.input.Text(
            uid='setting_app_secret',
            weight=20,
            label=_lang.t('facebook@app_secret'),
            required=True,
            help=_lang.t('facebook@app_secret_setup_help'),
            rules=_validation.rule.Regex(pattern='[0-9a-f]{32}'),
            default=app_secret,
        ))

        super()._on_setup_widgets()
