def instance_from_json(model, data):
    if not data:
        return None
    return model(data)


def to_json(response):
    if not response:
        return None
    return response.json()


class Token(object):
    """Model representing the authorized token retrieved
    from the API.

    Check https://www.azion.com.br/developers/api-v1/authentication/
    for more details.

    .. attribute:: token

        Generated token to authenticate API requests.

    .. attribute:: created_at

        Date when the token was created.

    .. attribute:: expires_at

        Date when the token will expire.
    """

    def __init__(self, data):
        self.load_data(data)

    def load_data(self, data):
        self.token = data['token']
        self.created_at = data['created_at']
        self.expires_at = data['expires_at']

    def __repr__(self):
        return f'<TokenAuth [{self.token[:6]}]>'


class Configuration(object):
    """Model representing the configuration retrieved
    from the API.

    .. attribute:: id

        Configuration's unique ID.

    .. attribute:: name

        Configuration name - a human representation to identify
        the configuration.

    .. attribute:: domain_name

        Domain name is an unique represenation of the configuration
        in the entire CDN.

    .. attribute:: active

        Wheter the configuration is currently deployed or not.

    .. attribute:: delivery_protocol

        Delivery Protocol is the protocol used to deliver the content
        through the CDN.

    .. attribute:: digital_certificate

        Digital's Certificate ID used to deliver the content using a
        SSL certificate.

    .. attribute:: rawlogs

        Whether RawLogs is enabled for this configuration.

    .. attribute:: cnames

        A list of domains used to represent your configuration, other than
        the domain_name.
    """

    def __init__(self, data):
        self.load_data(data)

    def load_data(self, data):
        self.id = data['id']
        self.name = data['name']
        self.domain_name = data['domain_name']
        self.active = data['active']
        self.delivery_protocol = data['delivery_protocol']
        self.digital_certificate = data['digital_certificate']
        self.cname_access_only = data['cname_access_only']
        self.rawlogs = data['rawlogs']
        self.cnames = data['cnames']
