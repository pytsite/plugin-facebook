"""PytSite Facebook Plugin Errors.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class AppIdNotSet(Exception):
    pass


class AppSecretNotSet(Exception):
    pass


class AuthSessionError(Exception):
    pass


class SessionError(Exception):
    pass


class OpenGraphError(Exception):
    pass
