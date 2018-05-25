from unittest import mock

import pytest

from azion import api
from azion.client import Azion


class TestAzionAPI(object):

    def test_login_using_token(self):
        with mock.patch.object(Azion, 'login') as login:
            entry_point = api.login(token='foobar')
            assert isinstance(entry_point, Azion)
            login.assert_called_once_with('foobar')

    def test_authorize_using_basic_credentials(self):
        with mock.patch('azion.api.Azion') as client:
            api.authorize(username='foo', password='bar')
            client().authorize.assert_called_once_with('foo', 'bar')
