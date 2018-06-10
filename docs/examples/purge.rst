==============
Purge examples
==============

If you need to remove content from Azion cache before it expires, use
the Purge API. You can use it to expire content based on your own business rules.

Purge by URL
------------

.. code-block:: python

    from azion import authorize, login

    # Authorize and login
    auth = authorize('myemail@mail.com', 'mysecretpassword')
    azion = login(auth.token)

    # Purge by URL using CNAME and Domain name
    # These two URLs will be purged from Azion cache
    my_urls = [
        'www.maugzoide.com/foobar.jpg'
        '11111a.ha.azioncdn.net/test.js'
    ]

    azion.purge_url(urls)

This endpoint answers with HTTP 207 (WebDAV). It is a multi-status code designed to represent
an answer that was partially OK.
In the result you can find that the dictionary keys are the status and the keys `urls` and `details`
will exist for every status code. To filter for responses that succeed/failed, we provide two methods:

.. code-block:: python

    result = azion.purge_url(urls)

    # URLs that were purged
    result.succeed()

    # URLs that were not purged
    result.failed()

Purge by Cache Key
------------------

You can purge using a cache key. A common example is purging an image.
Purging a URL like static.yourdomain.com/images/image.jpg@@ will include all variations
found after `image.jpg`

.. code-block:: python

    my_urls = [
        'www.maugzoide.com/profile.jpg@@'
        '11111a.ha.azioncdn.net/@@cookie_name=foobar'
    ]

    azion.purge_cache_key(urls)

Purge Wildcard
--------------

Use a wildcard purge to delete a list of objects from the cache.
This function accepts one URL only.

.. code-block:: python

    url = 'www.maugzoide.com/static/img/*'

    azion.purge_wildcard(url)
