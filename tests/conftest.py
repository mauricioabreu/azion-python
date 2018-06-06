"""Configuration for all test cases."""
import json
import os

import betamax

from betamax.serializers import JSONSerializer


class PrettyJSONSerializer(JSONSerializer):
    """Serializer that saves all cassettes
    in a human readable format, indenting and sorting keys."""
    name = 'prettyjson'

    def serialize(self, cassette_data):
        return json.dumps(
            cassette_data,
            sort_keys=True,
            indent=2,
            separators=(',', ': '),
        )


token = os.environ.get('AZ_TOKEN', 'foobar')

# Register pretty JSON serializer
betamax.Betamax.register_serializer(PrettyJSONSerializer)

with betamax.Betamax.configure() as config:
    # Directory to save/load requests and responses
    # executed by betamax
    config.cassette_library_dir = 'tests/integration/cassettes'
    # Change real token by this placeholder
    config.define_cassette_placeholder('<AUTH_TOKEN>', token)
    # Save formatted JSON instead of one line files
    config.default_cassette_options['serialize_with'] = 'prettyjson'
