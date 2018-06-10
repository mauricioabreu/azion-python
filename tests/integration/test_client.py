import itertools
import os

from azion.client import Azion
from azion.models import Configuration

import betamax

token = os.environ.get('AZ_TOKEN', 'foobar')


class TestConfiguration(object):

    def test_create_configuration(self):
        client = Azion(token)
        recorder = betamax.Betamax(client.session)

        with recorder.use_cassette('Configuration_create'):
            configuration = client.create_configuration(
                'Dummy configuration', 'www.example.com', 'ww2.example.com',
                cname=['www.example-cname.com'], delivery_protocol='http')

        assert isinstance(configuration, Configuration)
        assert configuration.active is True
        assert configuration.id
        assert configuration.cname == ['www.example-cname.com']
        assert configuration.digital_certificate is None
        assert configuration.rawlogs is False
        assert configuration.delivery_protocol == 'http'
        assert configuration.cname_access_only is False
        assert configuration.name == 'Dummy configuration'
        assert configuration.domain_name

    def test_get_configuration(self):
        client = Azion(token)
        recorder = betamax.Betamax(client.session)

        with recorder.use_cassette('Configuration_get'):
            configuration = client.get_configuration(1528252734)

        assert isinstance(configuration, Configuration)

    def test_update_configuration(self):
        client = Azion(token)
        recorder = betamax.Betamax(client.session)

        with recorder.use_cassette('Configuration_partial_update'):
            configuration = client.partial_update_configuration(
                1528252734, delivery_protocol='http,https')

        assert isinstance(configuration, Configuration)
        assert configuration.delivery_protocol == 'http,https'

    def test_replace_configuration(self):
        client = Azion(token)
        recorder = betamax.Betamax(client.session)

        with recorder.use_cassette('Configuration_replace'):
            configuration = client.replace_configuration(
                1528252734,
                name='Dummy configuration',
                delivery_protocol='http,https')

        assert isinstance(configuration, Configuration)
        assert configuration.delivery_protocol == 'http,https'

    def test_list_configurations(self):
        client = Azion(token)
        recorder = betamax.Betamax(client.session)

        with recorder.use_cassette('Configuration_list'):
            configurations = client.list_configurations()

        assert configurations
        assert isinstance(configurations, list)
        assert all(isinstance(configuration, Configuration)
                   for configuration in configurations)

    def test_delete_configuration(self):
        client = Azion(token)
        recorder = betamax.Betamax(client.session)

        with recorder.use_cassette('Configuration_delete'):
            assert client.delete_configuration(1528252734)


class TestPurge(object):

    def test_purge_url(self):
        client = Azion(token)
        recorder = betamax.Betamax(client.session)

        authorized_urls = [
            'www.maugzoide.com/foo.jgp', 'www.maugzoide.com/bar.jgp']
        forbidden_urls = ['www.notauthorize.com/mistaken.jgp']
        urls = authorized_urls + forbidden_urls

        with recorder.use_cassette('Purge_url'):
            purge = client.purge_url(urls)

        succeed_urls = itertools.chain(
            *[response['urls'] for response in purge.succeed().values()])
        assert sorted(authorized_urls) == sorted(list(succeed_urls))

        failed_urls = itertools.chain(
            *[response['urls'] for response in purge.failed().values()])
        assert sorted(forbidden_urls) == sorted(list(failed_urls))

    def test_purge_cache_key(self):
        client = Azion(token)
        recorder = betamax.Betamax(client.session)

        urls = [
            'www.maugzoide.com/@@cookie_name=foobar',
            'www.maugzoide.com/profile.jpg@@'
        ]

        with recorder.use_cassette('Purge_cachekey'):
            assert client.purge_cache_key(urls)

    def test_purge_wildcard(self):
        client = Azion(token)
        recorder = betamax.Betamax(client.session)

        url = 'www.maugzoide.com/static/img/*'

        with recorder.use_cassette('Purge_wildcard'):
            assert client.purge_wildcard(url)
