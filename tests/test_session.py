import requests

from azion.client import Session


class TestSession(object):

    def test_default_headers(self):
        session = Session()
        assert session.headers['Accept'] == 'application/json; version=1'
        assert session.headers['Accept-Charset'] == 'utf-8'
        assert session.headers['Content-Type'] == 'application/json'

    def test_token_auth(self):
        session = Session()
        session.token_auth('foobar')
        request = session.prepare_request(
            requests.Request('GET', 'https://api.azion.net/'))
        assert request.headers['Authorization'] == 'token foobar'
