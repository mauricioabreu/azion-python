=======================
Configurations examples
=======================

Here are some examples so you don't have to read the source to understand
how to use this client.

.. code-block:: python

    from azion import authorize, login

    # Authorize and login
    auth = authorize('myemail@mail.com', 'mysecrepassword')
    azion = login(auth.token)

    # Create a configuration
    azion.create_configuration(
        'My cool configuration',
        'www.myorigin.com',
        'www.myhostheader.com'
    )
