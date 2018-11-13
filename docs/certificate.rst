===========
Certificate
===========

These instructions will explain you about how to work with certificate upload and getting API.

Certificate model fields
========================

Certificate model in database contains next fields:

- Required:
    - ``id`` (uuid)
    - ``holder`` (ForeignKey to user, setting to Null, if user was deleted)
    - ``user_eth_address`` (CharField)
    - ``institution_title`` (CharField)
    - ``institution_link`` (URLField)
    - ``certificate_title`` (CharField)
    - ``granted_to_type`` (PositiveSmallIntegerField from 1 to 3)
    - ``ipfs_hash`` (CharField)

- Optional:
    - ``program_title`` (CharField)
    - ``course_link`` (URLField)
    - ``industries`` (ManyToManyField)
    - ``skills`` (ManyToManyField)
    - ``score`` (FloatField)
    - ``duration`` (PositiveSmallIntegerField)
    - ``expiration_date`` (DateTimeField)
    - ``checksum_hash`` (CharField)


Certificate View Set
====================

----------------------
Create new certificate
----------------------

Method ``create(self, request)`` acccepting POST requests with JSON information about new certificate.

Certificate file previously should be uploaded on IPFS.

**Returns**

- If ok:
    - Code status 200
    - ``certificate_pk`` JSON with Certificate id on bdn
- Else:
    - Code status 400
    - ``error`` JSON with errors

**Example**:

.. code-block:: javascript
    
    // POST Request to *your_bdn_host*/api/v1/certificates/

    '/api/v1/certificates/',
    data={
        'institution_title': 'test',
        'institution_link': 'http://example.com',
        'certificate_title': 'test',
        'holder_eth_address': '0xD2BE64317Eb1832309DF8c8C18B09871809f3735',
        'score': '',
        'duration': '',
        'skills': ['Python'],
        'ipfs_hash': 'Qme1WcHcEZU5uct9Wgfdn7S3mKbjSkvwdDTTfSUDjHTqjL'
    },
    HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
    HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'

--------------------
Get certificate info
--------------------

Method ``retrieve(self, request, pk=None)`` acccepting GET requests with certificate id and reply with JSON information about certificate.

**Returns**

- If ok:
    - Code status 200
    - JSON with Certificate data

**Example**

.. code-block:: javascript
    
    // GET Request to *your_bdn_host*/api/v1/certificates/(?P<pk>[^/.]+)/

    '/api/v1/certificates/e0e433e9-477e-43a3-8e23-dfe2686202be/',
    HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
    HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')

--------------------
Get certificate list
--------------------

Method ``list(self, request)`` acccepting GET requests reply with JSON information about certificates by issuer user.

**Returns**

- If ok:
    - Code status 200
    - JSON with Certificates list data by issuer user

**Example**

.. code-block:: javascript
    
    // GET Request to *your_bdn_host*/api/v1/certificates/

    '/api/v1/certificates/',
    HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
    HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'

---------------------------
Get certificates by learner
---------------------------

Method ``get_certificates_by_learner(self, request)`` acccepting GET requests with ``eth_address`` and reply with JSON information about certificates by learner ETH Address.

**Returns**

- If ok:
    - Code status 200
    - JSON with Certificates list data by learner ETH Address

**Example**

.. code-block:: javascript
    
    // GET Request to *your_bdn_host*/api/v1/certificates/get_certificates_by_learner/?eth_address=*some_eth_address*

    '/api/v1/certificates/?eth_address=0x00000',
    HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
    HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'


------------------------
Delete certificate by id
------------------------

Method ``delete_by_id(self, request, pk=None)`` acccepting POST requests with certificate id in line.

**Returns**

- If ok:
    - Code status 200
- Else if user is not holder:
    - Code status 401
- Else if certificate does not exist:
    - Code status 404

**Example**:

.. code-block:: javascript
    
    // POST Request to *your_bdn_host*/api/v1/certificates/(?P<pk>[^/.]+)/delete_by_id/

    '/api/v1/certificates/e0e433e9-477e-43a3-8e23-dfe2686202be/delete_by_id/',
    data={
    },
    HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
    HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'