from azion.responses import handle_multi_status


def test_handle_multi_status():
    # Response taken directly from API documentation
    # https://www.azion.com.br/developers/api-v1/real-time-purge/
    response = [
        {
            "status": "HTTP/1.1 201 CREATED",
            "urls": [
                "http://www.domain.com/",
                "http://www.domain.com/test.js"
            ],
            "details": "Purge request successfully created"
        },
        {
            "status": "HTTP/1.1 403 FORBIDDEN",
            "urls": ["http://static.mistaken-domain.com/image1.jpg"],
            "details": "Unauthorized domain for your account"
        }
    ]

    responses = handle_multi_status(response, 'urls')
    assert 201 in responses
    assert responses[201]['details'] == 'Purge request successfully created'
    assert responses[201]['urls'] == ['http://www.domain.com/', 'http://www.domain.com/test.js']
    assert responses.succeed()
    assert responses.failed()
