============
Verification
============

These instructions will explain you about how to work with verification API.

Verification model fields
=========================

Verification model in database contains next fields:

- Required:
    - ``id`` (uuid)
    - ``state`` (FSMField with chooses: ``requested``, ``open``, ``pending``, ``verified``, ``revoked`` and ``rejected``)
    - ``block_number`` (IntegerField)
    - ``granted_to_type`` (PositiveSmallIntegerField from 1 to 3)
    - ``verifier_type`` (PositiveSmallIntegerField from 1 to 3)
    - ``date_created`` (DateTimeField with auto add)
    - ``date_last_modified`` (DateTimeField with auto add now)

- Optional:
    - ``tx_hash`` (CharField)
    - ``block_hash`` (CharField)
    - ``certificate`` (ForeignKey to certificate, setting to Null, if certificate was deleted)
    - ``granted_to`` (ForeignKey to user, setting to Null, if user was deleted)
    - ``verifier`` (ForeignKey to user, setting to Null, if user was deleted)
    - ``meta_ipfs_hash`` (CharField)

Verification View Set
=====================

-----------------------
Create new verification
-----------------------

Method ``create(self, request)`` acccepting POST requests with JSON information about new verification.

**Returns**

- If ok:
    - Code status 200
    - JSON with Verification data on bdn
- Else:
    - Code status 400
    - ``error`` JSON with errors

**Example**:

.. code-block:: javascript
    
    // POST Request to *your_bdn_host*/api/v1/verifications/

    '/api/v1/verifications/',
    data={
        'verifier': '0x05',
        'granted_to_type': 1,
        'verifier_type': 2,
        'certificate': '0cb19a83-d3c9-491b-99a3-374ebb01c43f',
    },
    HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
    HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'

---------------------
Get verification info
---------------------

Method ``retrieve(self, request, pk=None)`` acccepting GET requests with verification id and reply with JSON information about verification.

**Returns**

- If ok:
    - Code status 200
    - JSON with Certificate data
- Else:
    - Code status 400

**Example**

.. code-block:: javascript
    
    // GET Request to *your_bdn_host*/api/v1/verifications/(?P<pk>[^/.]+)/

    '/api/v1/verifications/e0e433e9-477e-43a3-8e23-dfe2686202be/',
    HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
    HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')

----------------------
Get verifications list
----------------------

Method ``list(self, request)`` acccepting GET requests with inline get parameter ``active_profile``: (``'Academy'``, ``'Business'``, ``'Learner'``) and reply with JSON information about verification by verifier user.

**Returns**

- If ok:
    - Code status 200
    - JSON with Verifications list data by verifier user

**Example**:

.. code-block:: javascript
    
    // GET Request to *your_bdn_host*/api/v1/verifications/?active_profile=*String*

    '/api/v1/verifications/?active_profile=Academy',
    HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
    HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'

-----------------
Set state to open
-----------------

Method ``set_open_by_id(self, request, pk=None)`` acccepting POST requests with verification id in line. Isuuer should be verifier of this verification.

**Returns**

- If ok:
    - Code status 200
- Else:
    - Code status 404

**Example**:

.. code-block:: javascript
    
    // POST Request to *your_bdn_host*/api/v1/verifications/(?P<pk>[^/.]+)/set_open_by_id/

    '/api/v1/verifications/e0e433e9-477e-43a3-8e23-dfe2686202be/set_open_by_id/',
    data={
    },
    HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
    HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'

--------------------
Set state to pending
--------------------

Method ``set_pending_by_id(self, request, pk=None)`` acccepting POST requests with verification id in line. Isuuer should be verifier of this verification.

**Returns**

- If ok:
    - Code status 200
- Else:
    - Code status 404

**Example**

.. code-block:: javascript
    
    // POST Request to *your_bdn_host*/api/v1/verifications/(?P<pk>[^/.]+)/set_pending_by_id/

    '/api/v1/verifications/e0e433e9-477e-43a3-8e23-dfe2686202be/set_pending_by_id/',
    data={
    },
    HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
    HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'

---------------------
Set state to rejected
---------------------

Method ``reject_by_id(self, request, pk=None)`` acccepting POST requests with verification id in line. Isuuer should be verifier of this verification.

**Returns**

- If ok:
    - Code status 200
- Else:
    - Code status 404

**Example**

.. code-block:: javascript
    
    // POST Request to *your_bdn_host*/api/v1/verifications/(?P<pk>[^/.]+)/reject_by_id/

    '/api/v1/verifications/e0e433e9-477e-43a3-8e23-dfe2686202be/reject_by_id/',
    data={
    },
    HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
    HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'