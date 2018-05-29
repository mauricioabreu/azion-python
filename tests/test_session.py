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

    def test_build_url_with_default_url(self):
        session = Session()
        url = session.build_url('foo', 'bar', '1')
        assert url == 'https://api.azion.net/foo/bar/1'

    def test_build_url_with_different_base_url(self):
        session = Session()
        base_url = 'https://www.example.com'
        url = session.build_url('foo', 'bar', '1', base_url=base_url)
        assert url == 'https://www.example.com/foo/bar/1'
