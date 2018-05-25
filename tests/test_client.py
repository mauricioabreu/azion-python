from unittest import mock

import requests

from azion.client import Azion, Session


def create_mocked_session():
    MockedSession = mock.create_autospec(Session)
    session = MockedSession()
    base_attrs = ['headers', 'auth']
    attrs = dict(
        (key, mock.Mock()) for key in base_attrs
    )
    session.configure_mock(**attrs)
    session.delete.return_value = None
    session.get.return_value = None
    session.patch.return_value = None
    session.post.return_value = None
    session.put.return_value = None
    session.base_url = 'https://api.azion.net/'

    return session


class TestAzionClient(object):

    def test_login_using_token(self):
        mocked_session = create_mocked_session()
        client = Azion(session=mocked_session)
        client.login(token='foobar')
        mocked_session.token_auth.assert_called_once_with(token='foobar')

    def test_authorize(self):
        mocked_session = create_mocked_session()
        client = Azion(session=mocked_session)
        client.authorize('foo', 'bar')
        mocked_session.post.assert_called_once_with(
            'https://api.azion.net/tokens', data={}, auth=('foo', 'bar'))
