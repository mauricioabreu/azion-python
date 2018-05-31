import datetime

from azion import models


class TestModels(object):

    def test_filter_none(self):
        data = {'foo': False, 'bar': None}
        assert models.filter_none(data) == {'foo': False}

    def test_instance_from_json(self):

        class DummyModel(object):

            def __init__(self, data):
                self.data = data

        instance = models.instance_from_json(
            DummyModel, {'foobar': 1})
        assert isinstance(instance, DummyModel)

    def test_to_date(self):
        dt = datetime.datetime(
            2016, 11, 18, 14, 10, 58, 24903, tzinfo=datetime.timezone.utc)
        assert dt == models.to_date('2016-11-18T14:10:58.024903Z')


class TestConfiguration(object):

    def test_repr(self):
        data = {'id': 1, 'name': 'My cool configuration',
                'domain_name': '11111a.ha.azion.net', 'active': True,
                'delivery_protocol': 'http,https',
                'digital_certificate': None,
                'cname_access_only': False, 'rawlogs': False,
                'cname': ''}
        configuration = models.Configuration(data)
        assert repr(configuration) == '<Configuration [My cool configuration (11111a.ha.azion.net)]>'  # noqa
