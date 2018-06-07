Testing the client
==================

Every feature of a codebase must be tested if we want to be more confident about it.
Tests help to document what the code does and how it works. Need a new feature or need to change
the behavior of a current function? Tests are here to cover you.

Integration tests
-----------------

The purpose of an Integration test is to ensure that our code units, depending on other units, work as expected.
In our case, we need to test how our code behave when interacting to the real API. How does it handle real JSON responses?

To acomplish this task, we use `Betamax <https://github.com/betamaxpy/betamax>`_ library. It records real requests made to the API,
saves it as JSON and replays it next time, without hitting the production site again.

Here is an example on how to test the creation of a new configuration:

.. code-block:: python

    class TestConfiguration(object):

        def test_create_configuration(self):
            client = Azion(token)
            recorder = betamax.Betamax(client.session)

            with recorder.use_cassette('Configuration_create'):
                configuration = client.create_configuration(
                    'Dummy configuration', 'www.example.com', 'ww2.example.com',
                    cname=['www.example-cname.com'], delivery_protocol='http')
            assert isinstance(configuration, Configuration)

To create new tests, you need to export an environment variable named `AZ_TOKEN`.
If you are using `Bash shell` you can export the variable and then run the tests:

.. code-block:: bash

    AZ_TOKEN='mytoken'
    make test

Using `Fish shell` like me? No problems:

.. code-block:: fish

    set -x AZ_TOKEN 'mytoken'
    make test

It is necessary because your new tests will try to hit the production API to fetch the response.
After executing the test, a new `cassette` will be generated. Your patch must contain these files.

Cassettes
~~~~~~~~~

`Cassettes` are the files used to store/load requests and responses. A good convention is to name them with the resource capitalized
and the action of the API function in lowercase, for example: ``Configuration_create``

Unit tests
----------

Fast feedback can be given by unit tests. These are tests used to cover units of code in isolation - they should not depend on other components.
And to achieve this goal, we must not rely on third party results like JSON responses obtained over a unreliable network.

`Mocking` the response is the right way to go here, ensuring that we called our function with the right parameters.
