.. Azion API documentation master file, created by
   sphinx-quickstart on Mon May 21 00:26:00 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===============================================
azion-python: interacting with Azion's ReST API
===============================================

`azion-python` is a library to interact with `Azion's ReST API`.

With this library you will be able to use the ReST API using a pythonic approach,
handling Python objects (models) instead of raw JSON responses.

.. code-block:: python

    from azion.api import authorize, login

    # Retrieve a new token
    auth = authorize('myemail@mail.com', 'mysecrepassword')

    # Login using the token
    azion = login(auth.token)

    # Retrieve a configuration
    configuration = azion.get_configuration(1028910)

    print(configuration.name)

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Installation
============

.. code-block:: console

    $ pip install azion-python

API
===

.. toctree::
    :maxdepth: 2

    api/index

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`