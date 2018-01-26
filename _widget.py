"""PytSite Facebook Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from datetime import datetime as _datetime
from pytsite import html as _html, router as _router, lang as _lang
from plugins import widget as _widget, assetman as _assetman
from ._session import AuthSession as _AuthSession, Session as _Session
from . import _api


class Auth(_widget.Abstract):
    """Authorization Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._app_id = kwargs.get('app_id') or _api.get_app_id()
        self._app_secret = kwargs.get('app_secret') or _api.get_app_secret()
        self._scope = kwargs.get('scope', 'public_profile,email,user_friends')
        self._access_token = kwargs.get('access_token', '')
        self._access_token_type = kwargs.get('access_token_type', '')
        self._access_token_expires = kwargs.get('access_token_expires', 0)
        self._user_id = kwargs.get('user_id', '')
        self._pages = []
        self._page_id = kwargs.get('page_id', '')
        self._screen_name = kwargs.get('screen_name', '')
        self._redirect_url = kwargs.get('redirect_url', _router.current_url())

        self._css += ' widget-facebook-oauth'

    @property
    def access_token(self) -> str:
        return self._access_token

    @property
    def access_token_type(self) -> str:
        return self._access_token_type

    @property
    def access_token_expires(self) -> str:
        return self._access_token_expires

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def pages(self) -> tuple:
        return tuple(self._pages)

    @property
    def page_id(self) -> str:
        return self._page_id

    @property
    def screen_name(self) -> str:
        return self._screen_name

    def _get_element(self, **kwargs) -> _html.Element:
        """Get HTML element representation of the widget.
        :param **kwargs:
        """
        # 'state' and 'code' typically received after successful Facebook authorization redirect
        inp = _router.request().inp
        state = inp.get('state')
        auth_code = inp.get('code')

        # Try to fetch access token from Facebook
        if not self._access_token and (state and auth_code):
            t_info = _AuthSession(state).get_access_token(auth_code)
            self._access_token = t_info['access_token']
            self._access_token_type = t_info['token_type']

            self._access_token_expires = float(t_info.get('expires_in', 0))
            if self._access_token_expires:
                self._access_token_expires = int(_datetime.now().timestamp() + self._access_token_expires)

            me = _Session(self._access_token).me()
            self._user_id = me['id']
            self._screen_name = me['name']

        # Pages
        if self._access_token:
            for acc in _Session(self._access_token).accounts():
                if 'CREATE_CONTENT' in acc['perms']:
                    self._pages.append((acc['id'], acc['name']))

        # Link to user profile or to facebook authorization URL
        if self._user_id and self._screen_name:
            a = _html.A(self._screen_name, href='https://facebook.com/' + self._user_id, target='_blank')
            a.append(_html.I(css='fa fa-facebook-square'))
        else:
            a = _html.A(href=_AuthSession(redirect_uri=self._redirect_url).get_authorization_url(self._scope))
            a.append(_html.Img(src=_assetman.url('facebook@img/facebook-login-button.png')))

        container = _widget.Container(self.uid)
        container.append_child(_widget.static.Text(
            self.uid + '[auth_url]',
            weight=10,
            label=_lang.t('facebook@user'), title=a.render()
        ))

        # Page select
        if self.pages:
            container.append_child(_widget.select.Select(
                self.uid + '[page_id]',
                weight=20,
                value=self._page_id,
                label=_lang.t('facebook@page'),
                items=self.pages,
                h_size='col-sm-6'
            ))

        container.append_child(_widget.input.Hidden(self.uid + '[access_token]', value=self.access_token))
        container.append_child(_widget.input.Hidden(self.uid + '[access_token_type]', value=self.access_token_type))
        container.append_child(
            _widget.input.Hidden(self.uid + '[access_token_expires]', value=self.access_token_expires))
        container.append_child(_widget.input.Hidden(self.uid + '[user_id]', value=self.user_id))
        container.append_child(_widget.input.Hidden(self.uid + '[screen_name]', value=self.screen_name))

        return container.get_element()
