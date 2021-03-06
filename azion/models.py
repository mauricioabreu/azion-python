import pendulum

from azion import exceptions


def instance_from_data(model, data):
    if not data:
        return None
    return model(data)


def many_of(model, data):
    if not data:
        return []
    return [instance_from_data(model, resource) for
            resource in data]


def decode_json(response, excepted_status_code):
    """Decode a JSON response.

    It wraps the `requests` json response decoder and
    adds a goodie to raise proper errors when the status
    code of the HTTP requests indicates client issues.

    :param object response:
        A `requests` response object.
    :param int excepted_status_code:
        HTTP status code expected after making the request.
        In case it differs, raise a right exception for the error.
    """

    # Bad request is interpreted as a falsey value.
    # So we compare it with `None`.
    if response is None:
        return None

    status_code = response.status_code
    if status_code != excepted_status_code:
        if status_code >= 400:
            raise exceptions.handle_error(response)

    return response.json()


def as_boolean(response, expected_status_code):
    if response:
        if response.status_code == expected_status_code:
            return True
        if response.status_code >= 400:
            raise exceptions.handle_error(response)
    return False


def filter_none(data):
    return {key: value for key, value in data.items() if value is not None}


def to_date(date):
    """Convert a string to a datetime object.

    :param str date: ISO 8601 string.
    :returns:
        datetime object
    :rtype:
        pendulum.datetime.DateTime
    """
    return pendulum.parse(date)


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
        self.created_at = to_date(data['created_at'])
        self.expires_at = to_date(data['expires_at'])

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

    def __repr__(self):
        return f'<Configuration [{self.name} ({self.domain_name})]>'

    def load_data(self, data):
        self.id = data['id']
        self.name = data['name']
        self.domain_name = data['domain_name']
        self.active = data['active']
        self.delivery_protocol = data['delivery_protocol']
        self.digital_certificate = data['digital_certificate']
        self.cname = data['cname']
        self.cname_access_only = data['cname_access_only']
        self.rawlogs = data['rawlogs']


class Address(object):
    """Model representing an Address - a related resource
    of `Origin` model.

    .. attribute:: address
        Hostname (FQDN) or IP address.

    .. attribute:: weigth
        Define how much traffic a server can handle,
        in comparison to the others (Load Balancer).

    .. attribute:: server_role
        Define how this origin will be used.

    .. attribute:: is_active
        Define whether this origin is active.
    """

    def __init__(self, data):
        self.load_data(data)

    def load_data(self, data):
        self.address = data['address']
        self.weight = data['weight']
        self.server_role = data['server_role']
        self.is_active = data['is_active']


class Origin(object):
    """Model representing the Origin retrieved
    from the API.

    .. attribute:: id
        Origin's unique ID.

    .. attribute:: name
        Origin name

    .. attribute:: origin_type
        Origin type.

    .. attribute:: method
        Define how the CDN will handle load balancer
        connections.

    .. attribute:: host_header
        Host header will be sent to your origin.

    .. attribute:: origin_protocol_policy
        Define the protocol CDN will use to connect
        to your origin.

    .. attribute:: addresses
        A list of `Address` resources.
        These are the address used by Azion CDN to
        access the content will be cached and delivered.

    .. attribute:: connection_timeout
        Timeout when connection to the origin (seconds).

    .. attribute:: timeout_between_bytes
        Timeout for a connection without data transferring (seconds).
    """

    def __init__(self, data):
        self.load_data(data)

    def __repr__(self):
        return f'<Origin [{self.name}]>'

    def load_data(self, data):
        self.id = data['id']
        self.name = data['name']
        self.origin_type = data['origin_type']
        self.method = data['method']
        self.host_header = data['host_header']
        self.origin_protocol_policy = data['origin_protocol_policy']
        self.addresses = many_of(Address, data['addresses'])
        self.connection_timeout = data['connection_timeout']
        self.timeout_between_bytes = data['timeout_between_bytes']
