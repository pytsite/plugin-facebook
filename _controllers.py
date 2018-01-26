"""PytSite Facebook Plugin Endpoints.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import router as _router, routing as _routing
from ._session import AuthSession as _AuthSession


class Authorize(_routing.Controller):
    def exec(self):
        """Authorization.
        """
        # Check for errors
        error = self.arg('error_description')
        if error:
            _router.session().add_error_message(error)

        # Initializing authorization session
        auth_session = _AuthSession(self.arg('state'))

        return self.redirect(_router.url(auth_session.redirect_uri, query=self.args))
