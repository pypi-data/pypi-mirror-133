Aplazame Python Sdk
===================

|Build Status|

|Aplazame|

`Aplazame`_, a consumer credit company, offers a payment system that can be
used by online buyers to receive funding for their purchases.

Installation
------------

To install aplazame-sdk, simply:

.. code:: sh

    $ pip install aplazame-sdk

Usage
-----

.. code:: python

    >>> import aplazame_sdk
    >>> client = aplazame_sdk.Client('token', sandbox=True, version='1', ctype='json')
    >>> r = client.orders(page=2)
    >>> r.json()
    {
      "cursor": {
        "after": 3,
        "before": 1
      },
      "paging": {
        "count": 314,
        "next": "https://api.aplazame.com/orders?page=3",
        "previous": "https://api.aplazame.com/orders?page=1"
      },
      "results": [
      ]
    }
    >>> r.status_code
    200

Exceptions
----------

.. code:: python

    >>> import aplazame_sdk
    >>> client = aplazame_sdk.Client('token')
    >>> try:
    ...     r = client.get_order('buh')
    ... except aplazame_sdk.AplazameError as err:
    ...     err.code
    404

Http
----

.. code:: http

    GET /orders HTTP/1.1
    Accept: application/vnd.aplazame.sandbox.v1+json
    Authorization: Bearer ->token<-
    Host: api.aplazame.com

    HTTP/1.1 200 OK
    Content-Type: application/vnd.aplazame.sandbox.v1+json

Documentation
-------------

Documentation is available at `docs.aplazame.com`_.

.. _Aplazame: https://aplazame.com
.. _docs.aplazame.com: http://docs.aplazame.com

.. |Build Status| image:: https://img.shields.io/pypi/v/aplazame-sdk.svg
   :target: https://pypi.python.org/pypi/aplazame-sdk
.. |Aplazame| image:: https://aplazame.com/landing-assets/images/banners/banner-1517-white.png
   :target: https://aplazame.com
