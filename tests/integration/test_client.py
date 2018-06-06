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
