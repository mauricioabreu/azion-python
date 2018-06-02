import json


from azion.exceptions import BadRequest, handle_error


class Response(object):

    def json(self):
        return {'detail': ['Invalid foo']}


class TestExceptions(object):

    def test_handle_error(self):
        response = Response()
        response.status_code = 400
        error = handle_error(response)
        assert isinstance(error, BadRequest)
        assert error.errors == ['Invalid foo']
        assert error.status_code == 400
        assert response == error.response
        assert repr(error) == '<BadRequest [400]>'
