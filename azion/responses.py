class MultiStatus(dict):
    """A container acting like a dict to
    save responses with multiple status. Since multi-status proposal
    recommends to keep the status as a identifier, we are using a dict
    to group responses by status."""

    def succeed(self):
        """Filter succeed purges.

        :return: succeed respones.
        :rtype: dict
        """
        return {201: self[201]}

    def failed(self):
        """Filter failed purges.

        :return: failed responses.
        :rtype: dict
        """
        return {status: response for status, response in
                self.items() if status >= 400}


def handle_multi_status(response, field):
    """Handle multi-status response.

    A multi-status response conveys information about multiple resources
    in situations where multiple status codes might be appropriate.

    :param dict response:
        A data structure containing a key `status` referencing the
        HTTP status code.
    :param str field:
        Which field is related to the error, essential value to know
        what went right and wrong.
    """
    responses = MultiStatus()
    for item in response:
        status = parse_status_code(item['status'])
        responses.update({
            status: {
                'details': item['details'],
                field: item[field]
            }
        })
    return responses


def parse_status_code(verbose_status):
    """Parse a HTTP status code like `HTTP/1.1 201 CREATED`
    and return only 201 instead."""
    pieces = verbose_status.split(' ')
    return int(pieces[1])
