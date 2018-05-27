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
