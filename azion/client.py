"""Client to access and interact with Azion's API."""
import requests

from azion.models import (
    Configuration, Token, instance_from_json, to_json)


class AuthToken(requests.auth.AuthBase):
    """Custom class for token based authorization."""

    def __init__(self, token):
        """
        :param str token: Authorization token. It can be
            obtained from :func:`~azion.client.Azion.token_auth`
        """
        self.token = token

    def __call__(self, request):
        """Update request with additional headers."""
        request.headers['Authorization'] = f'token {self.token}'
        return request


class Session(requests.Session):
    auth = None

    def __init__(self):
        super(Session, self).__init__()
        self.headers.update({
            'Accept': 'application/json; version=1',
            'Accept-Charset': 'utf-8',
            'Content-Type': 'application/json'
        })
        self.base_url = 'https://api.azion.net/'

    def token_auth(self, token):
        self.auth = AuthToken(token)


class Azion(object):
    """Entrypoint to work with Azion API."""

    def __init__(self, token=None, session=None):
        """Create a new Azion API instance.

        :param str token: Authorization token. It can be
            obtained from :func:`~azion.client.Azion.token_auth`
        """
        self.session = session or Session()

        if token:
            self.login(token)

    def login(self, token):
        """Log the user into Azion's API.

        :param str token: Authorization token. It can be
            obtained from :func:`~azion.client.Azion.token_auth`
        """
        self.session.token_auth(token)

    def authorize(self, username, password):
        """Obtain a fresh token to handle Azion's API protected calls.

        :param str username:
            username
        :param str password:
            password
        """
        url = f'{self.session.base_url}tokens'
        response = self.session.post(url, data={}, auth=(username, password))
        json = to_json(response)
        return instance_from_json(Token, json)

    def get_configuration(self, configuration_id):
        """Retrieve a configuration.

        :param int configuration_id: configuration id
        """
        url = f'{self.session.base_url}content_delivery/configurations/{configuration_id}'
        response = self.session.get(url)
        json = to_json(response)
        return instance_from_json(Configuration, json)
