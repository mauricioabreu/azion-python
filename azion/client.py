"""Client to access and interact with Azion's API."""
import requests

from azion.__metadata__ import __version__ as version
from azion.models import (
    Configuration, Token, as_boolean,
    decode_json, filter_none, instance_from_data, many_of)
from azion.responses import handle_multi_status


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
            'Content-Type': 'application/json',
            'User-Agent': f'azion-python/{version}'
        })
        self.base_url = 'https://api.azion.net'

    def token_auth(self, token):
        self.auth = AuthToken(token)

    def build_url(self, *args, **kwargs):
        """Build a URL depending on the `base_url`
        attribute."""
        params = [kwargs.get('base_url') or self.base_url]
        params.extend(args)
        params = map(str, params)
        return '/'.join(params)


class Azion(object):
    """Entrypoint to work with Azion API.

    To start using this client, we need a valid token.
    For this we can use the `authorize` function:

    .. code-block:: python

        from azion.api import authorize, login
        auth = authorize(user, password)
        azion = login(auth.token)

    Now you can use all API resources.
    """

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
        url = self.session.build_url('tokens')
        response = self.session.post(url, data={}, auth=(username, password))
        json = decode_json(response, 201)
        return instance_from_data(Token, json)

    def get_configuration(self, configuration_id):
        """Retrieve a configuration.

        :param int configuration_id: configuration id
        """
        url = self.session.build_url(
            'content_delivery', 'configurations', configuration_id)
        response = self.session.get(url)
        json = decode_json(response, 200)
        return instance_from_data(Configuration, json)

    def list_configurations(self):
        """List configurations."""
        url = self.session.build_url('content_delivery', 'configurations')
        response = self.session.get(url)
        json = decode_json(response, 200)
        return many_of(Configuration, json)

    def create_configuration(self, name, origin_address, origin_host_header,
                             cname=None, cname_access_only=False,
                             delivery_protocol='http',
                             digital_certificate=None,
                             origin_protocol_policy='preserve',
                             browser_cache_settings=False,
                             browser_cache_settings_maximum_ttl=0,
                             cdn_cache_settings='honor',
                             cdn_cache_settings_maximum_ttl=0):
        """Create a configuration.

        :param str name: human-readable name for the configuration.
        :param str origin_address: origin address that can be an IP
            or a hostname (FQDN)
        :param str origin_host_header: host header will be sent to the origin.
        :param list cname: a list os strings containing all cnames.
            Default empty string.
        :param bool cname_access_only: defines whether the content delivery
            should be done only through cnames. Default to False.
        :param str delivery_protocol: defines the HTTP protocol used
            to deliver content. Default to http.
        :param int digital_certificate: Digital Certificate ID.
            Check `Digital Certificates`_ for more info.
        :param str origin_protocol_policy: Protocol policy used to connect
            to the origin.
        :param bool browser_cache_settings: whether the user browser should
            respect the cache headers sent from the origin. Default to False.
        :param int browser_cache_settings_maximum_ttl: used within
            `browser_cache_settings`, defines how many seconds
            browser cache object will live. Default to 0.

        .. _Digital Certificates:
            https://www.azion.com.br/developers/documentacao/produtos/content-delivery/digital-certificates/
        """
        data = {
            'name': name, 'origin_address': origin_address,
            'origin_host_header': origin_host_header,
            'cname': cname, 'cname_access_only': cname_access_only,
            'delivery_protocol': delivery_protocol,
            'digital_certificate': digital_certificate,
            'origin_protocol_policy': origin_protocol_policy,
            'browser_cache_settings': browser_cache_settings,
            'browser_cache_settings_maximum_ttl': browser_cache_settings_maximum_ttl,
            'cdn_cache_settings': cdn_cache_settings,
            'cdn_cache_settings_maximum_ttl': cdn_cache_settings_maximum_ttl
        }

        url = self.session.build_url('content_delivery', 'configurations')
        response = self.session.post(url, json=filter_none(data))
        json = decode_json(response, 201)
        return instance_from_data(Configuration, json)

    def delete_configuration(self, configuration_id):
        """Delete a configuration.

        :param int configuration_id:
            Configuration ID.
        """
        url = self.session.build_url(
            'content_delivery', 'configurations', configuration_id)
        response = self.session.delete(url)
        return as_boolean(response, 204)

    def partial_update_configuration(self, configuration_id, name=None,
                                     cname=None, cname_access_only=None,
                                     delivery_protocol=None,
                                     digital_certificate=None,
                                     rawlogs=None, active=None):
        """Partially updates a configuration.

        One or more fields can be updated, without changing the current
        values of the other fields of this configuration.

        :param str name: human-readable name for the configuration.
        :param list cname: a list os strings containing all cnames.
            Default empty string.
        :param bool cname_access_only: defines whether the content delivery
            should be done only through cnames. Default to False.
        :param str delivery_protocol: defines the HTTP protocol used
            to deliver content. Default to http.
        :param int digital_certificate: Digital Certificate ID.
            Check `Digital Certificates`_ for more info.
        :param boolean rawlogs:
            Whether this configuration will store logs in the Cloud Storage.
        :param boolean active:
            Whether this configuration is active.

        .. _Digital Certificates:
            https://www.azion.com.br/developers/documentacao/produtos/content-delivery/digital-certificates/
        """

        data = {
            'name': name,
            'cname': cname, 'cname_access_only': cname_access_only,
            'delivery_protocol': delivery_protocol,
            'digital_certificate': digital_certificate,
            'rawlogs': rawlogs,
            'active': active
        }

        url = self.session.build_url(
            'content_delivery', 'configurations', configuration_id)
        response = self.session.patch(url, json=filter_none(data))
        json = decode_json(response, 200)
        return instance_from_data(Configuration, json)

    def replace_configuration(self, configuration_id, name=None,
                              cname=None, cname_access_only=None,
                              delivery_protocol=None,
                              digital_certificate=None,
                              rawlogs=None, active=None):
        """Replace a configuration.

        One or more fields can be updated. Fields that were not specificed
        in the request will be replaced for default values. Consider using
        :func:`~partial_update_configuration`

        :param str name: human-readable name for the configuration.
        :param list cname: a list os strings containing all cnames.
            Default empty string.
        :param bool cname_access_only: defines whether the content delivery
            should be done only through cnames. Default to False.
        :param str delivery_protocol: defines the HTTP protocol used
            to deliver content. Default to http.
        :param int digital_certificate: Digital Certificate ID.
            Check `Digital Certificates`_ for more info.
        :param boolean rawlogs:
            Whether this configuration will store logs in the Cloud Storage.
        :param boolean active:
            Whether this configuration is active.

        .. _Digital Certificates:
            https://www.azion.com.br/developers/documentacao/produtos/content-delivery/digital-certificates/
        """

        data = {
            'name': name,
            'cname': cname, 'cname_access_only': cname_access_only,
            'delivery_protocol': delivery_protocol,
            'digital_certificate': digital_certificate,
            'rawlogs': rawlogs,
            'active': active
        }

        url = self.session.build_url(
            'content_delivery', 'configurations', configuration_id)
        response = self.session.put(url, json=filter_none(data))
        json = decode_json(response, 200)
        return instance_from_data(Configuration, json)

    def purge_url(self, urls, method='delete'):
        """Purge content of the given URLs inside
        the `urls` list.

        :param list urls:
            List of URLs to be purged.
        :param str method:
            How the content will be purged.
            Default to 'delete'.
        """
        url = self.session.build_url('purge', 'url')
        response = self.session.post(
            url, json={'urls': urls, 'method': method})
        data = decode_json(response, 207)
        return handle_multi_status(data, 'urls')

    def purge_cache_key(self, urls, method='delete'):
        """Purge content of the given URLs inside
        the `urls` list. With this purge endpoint you
        can pass `cache keys`.

        :param list urls:
            List of URLs to be purged.
        :param str method:
            How the content will be purged.
            Default to 'delete'.
        """
        url = self.session.build_url('purge', 'cachekey')
        response = self.session.post(
            url, json={'urls': urls, 'method': method})
        return as_boolean(response, 201)

    def purge_wildcard(self, url, method='delete'):
        """Purge content of the given URL.
        With this purge endpoint you can use a wildcard (*)
        to remove all objects matching the URL.

        :param str url:
            Wildcard URL to be purged.
        :param str method:
            How the content will be purged.
            Default to 'delete'.
        """
        api_url = self.session.build_url('purge', 'wildcard')
        response = self.session.post(
            api_url, json={'urls': [url], 'method': method})
        return as_boolean(response, 201)
