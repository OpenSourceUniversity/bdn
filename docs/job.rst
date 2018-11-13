===
Job
===

These instructions will explain you about how to work with jobs upload and getting API.

Job model fields
================

Job model in database contains next fields:

- Required:
    - ``id`` (uuid)
    - ``title`` (CharField)
    - ``location`` (CharField)
    - ``overview`` (TextField)
    - ``description`` (TextField)
    - ``posted`` (DateField auto_now_add=True)
    - ``is_featured`` (BooleanField)

- Optional:
    - ``salary`` (CharField)
    - ``image_url`` (URLField)
    - ``company`` (ForeignKey to Company, setting to Null, if Company was deleted)
    - ``industries`` (ManyToManyField)
    - ``skills`` (ManyToManyField)
    - ``closes`` (DateField)
    - ``experience`` (CharField)
    - ``hours`` (PositiveSmallIntegerField)
    - ``languages`` (ArrayField of CharFields)

Job View Set
============

--------------
Create new job
--------------

Method ``create(self, request)`` acccepting POST requests with JSON information about new job.

**Returns**

- If ok:
    - Code status 200
    - ``pk`` JSON with Job id on bdn
- Else:
    - Code status 400
    - ``error`` JSON with errors

**Example**:

.. code-block:: javascript
    
    // POST Request to *your_bdn_host*/api/v1/jobs/

    '/api/v1/jobs/',
    data={
        'title': 'test',
        'location': 'test',
        'overview': 'test',
        'description': 'test',
        'hours': 1,
    },
    HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
    HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'

------------
Get job info
------------

Method ``retrieve(self, request, pk=None)`` acccepting GET requests with job id and reply with JSON information about job and company academy profile.

**Returns**

- If ok:
    - Code status 200
    - JSON with Job data and Academy data

**Example**

.. code-block:: javascript
    
    // GET Request to *your_bdn_host*/api/v1/jobs/(?P<pk>[^/.]+)/

    '/api/v1/jobs/e0e433e9-477e-43a3-8e23-dfe2686202be/',
    HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
    HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')

-------------
Get jobs list
-------------

Method ``list(self, request)`` acccepting GET requests reply with JSON information about jobs.

**Returns**

- If ok:
    - Code status 200
    - JSON with Jobs list data

**Example**

.. code-block:: javascript
    
    // GET Request to *your_bdn_host*/api/v1/jobs/

    '/api/v1/jobs/',
    HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
    HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'

-------------
Get job by id
-------------

Method ``get_by_id(self, request, pk=None)`` acccepting GET requests with job id and reply with JSON information about job.

**Returns**

- If ok:
    - Code status 200
    - JSON with Job data

**Example**

.. code-block:: javascript
    
    // GET Request to *your_bdn_host*/api/v1/jobs/(?P<pk>[^/.]+)/get_by_id/

    '/api/v1/jobs/e0e433e9-477e-43a3-8e23-dfe2686202be/get_by_id/',
    HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
    HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')

-------------------
Get jobs by company
-------------------

Method ``get_by_company(self, request)`` acccepting GET requests with inline ``eth_address`` and reply with JSON information about jobs by this company.

**Returns**

- If ok:
    - Code status 200
    - JSON with Jobs data

**Example**

.. code-block:: javascript
    
    // GET Request to *your_bdn_host*/api/v1/jobs/get_by_company/?eth_address=*some_addres*

    '/api/v1/jobs/get_by_company/?eth_address=0x000',
    HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
    HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')

--------------
Edit job by id
--------------

Method ``edit_by_id(self, request, pk=None)`` acccepting POST requests with new JSON information about job and inline id.

**Returns**

- If ok:
    - Code status 200

-Else if user is not creator of this job:
    - Code status 401

- Else:
    - Code status 400
    - ``error`` JSON with errors

**Example**:

.. code-block:: javascript
    
    // POST Request to *your_bdn_host*/api/v1/jobs/(?P<pk>[^/.]+)/edit_by_id/

    '/api/v1/jobs/e0e433e9-477e-43a3-8e23-dfe2686202be/edit_by_id/',
    data={
        'title': 'test',
        'location': 'test',
        'overview': 'test',
        'description': 'test',
        'hours': 1,
    },
    HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
    HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'

--------------------
Mark job as featured
--------------------

Method ``mark_featured_by_id(self, request, pk=None)`` acccepting POST requests with inline id.

**Returns**

- If ok:
    - Code status 200

-Else if user is not creator of this job:
    - Code status 401

**Example**:

.. code-block:: javascript
    
    // POST Request to *your_bdn_host*/api/v1/jobs/(?P<pk>[^/.]+)/mark_featured_by_id/

    '/api/v1/jobs/e0e433e9-477e-43a3-8e23-dfe2686202be/mark_featured_by_id/',
    data={
    },
    HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
    HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'

----------------
Delete job by id
----------------

Method ``delete_by_id(self, request, pk=None)`` acccepting POST requests with inline id.

**Returns**

- If ok:
    - Code status 200

-Else if user is not creator of this job:
    - Code status 401

**Example**:

.. code-block:: javascript
    
    // POST Request to *your_bdn_host*/api/v1/jobs/(?P<pk>[^/.]+)/delete_by_id/

    '/api/v1/jobs/e0e433e9-477e-43a3-8e23-dfe2686202be/delete_by_id/',
    data={
    },
    HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
    HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'