from unittest import mock

import requests

from azion.client import Azion, Session


def build_url(*args, **kwargs):
    """Mock `build_url` by injecting the real function
    right in the session object.
    """
    return Session().build_url(*args, **kwargs)


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
    session.base_url = 'https://api.azion.net'
    session.build_url = build_url

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

    def test_get_configuration(self):
        mocked_session = create_mocked_session()
        client = Azion(session=mocked_session)
        client.get_configuration(1)
        mocked_session.get.assert_called_once_with(
            'https://api.azion.net/content_delivery/configurations/1'
        )

    def test_create_configuration(self):
        mocked_session = create_mocked_session()
        client = Azion(session=mocked_session)
        client.create_configuration(
            'Dummy configuration', 'www.example.com', 'ww2.example.com')
        mocked_session.post.assert_called_once_with(
            'https://api.azion.net/content_delivery/configurations',
            json={
                'name': 'Dummy configuration',
                'origin_address': 'www.example.com',
                'origin_host_header': 'ww2.example.com',
                'cname_access_only': False,
                'delivery_protocol': 'http',
                'origin_protocol_policy': 'preserve',
                'browser_cache_settings': False,
                'browser_cache_settings_maximum_ttl': 0,
                'cdn_cache_settings': 'honor',
                'cdn_cache_settings_maximum_ttl': 0
            }
        )

    def test_delete_configuration(self):
        mocked_session = create_mocked_session()
        client = Azion(session=mocked_session)
        client.delete_configuration(1)
        mocked_session.delete.assert_called_once_with(
            'https://api.azion.net/content_delivery/configurations/1'
        )
