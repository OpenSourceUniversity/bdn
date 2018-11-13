======
Course
======

These instructions will explain you about how to work with courses upload and getting API.

Course model fields
===================

Course model in database contains next fields:

- Required:
    - ``id`` (uuid)
    - ``title`` (CharField)
    - ``description`` (TextField)
    - ``external_link`` (URLField)
    - ``is_featured`` (BooleanField)

- Optional:
    - ``program_title`` (CharField)
    - ``image_url`` (URLField)
    - ``provider`` (ForeignKey to Provider, setting to Null, if Provider was deleted)
    - ``tutor`` (CharField)
    - ``industries`` (ManyToManyField)
    - ``skills`` (ManyToManyField)
    - ``duration`` (PositiveSmallIntegerField)

Course View Set
===============

-----------------
Create new course
-----------------

Method ``create(self, request)`` acccepting POST requests with JSON information about new course.

**Returns**

- If ok:
    - Code status 200
    - ``pk`` JSON with Course id on bdn
- Else:
    - Code status 400
    - ``error`` JSON with errors

**Example**:

.. code-block:: javascript
    
    // POST Request to *your_bdn_host*/api/v1/courses/

    '/api/v1/courses/',
    data={
        'title': 'test',
        'description': 'test',
        'external_link': 'http://example.com/',
    },
    HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
    HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'

---------------
Get course info
---------------

Method ``retrieve(self, request, pk=None)`` acccepting GET requests with course id and reply with JSON information about course and provider academy profile.

**Returns**

- If ok:
    - Code status 200
    - JSON with Course data and Academy data

**Example**

.. code-block:: javascript
    
    // GET Request to *your_bdn_host*/api/v1/courses/(?P<pk>[^/.]+)/

    '/api/v1/courses/e0e433e9-477e-43a3-8e23-dfe2686202be/',
    HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
    HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')

----------------
Get courses list
----------------

Method ``list(self, request)`` acccepting GET requests reply with JSON information about courses.

**Returns**

- If ok:
    - Code status 200
    - JSON with Courses list data

**Example**

.. code-block:: javascript
    
    // GET Request to *your_bdn_host*/api/v1/courses/

    '/api/v1/courses/',
    HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
    HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'

----------------
Get course by id
----------------

Method ``get_by_id(self, request, pk=None)`` acccepting GET requests with course id and reply with JSON information about course.

**Returns**

- If ok:
    - Code status 200
    - JSON with Course data

**Example**

.. code-block:: javascript
    
    // GET Request to *your_bdn_host*/api/v1/courses/(?P<pk>[^/.]+)/get_by_id/

    '/api/v1/courses/e0e433e9-477e-43a3-8e23-dfe2686202be/get_by_id/',
    HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
    HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')

-----------------------
Get courses by provider
-----------------------

Method ``get_by_provider(self, request)`` acccepting GET requests with inline ``eth_address`` and reply with JSON information about courses by this provider.

**Returns**

- If ok:
    - Code status 200
    - JSON with Courses data

**Example**

.. code-block:: javascript
    
    // GET Request to *your_bdn_host*/api/v1/courses/get_by_provider/?eth_address=*some_addres*

    '/api/v1/courses/get_by_provider/?eth_address=0x000',
    HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
    HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')

-----------------
Edit course by id
-----------------

Method ``edit_by_id(self, request, pk=None)`` acccepting POST requests with new JSON information about course and inline id.

**Returns**

- If ok:
    - Code status 200

-Else if user is not creator of this course:
    - Code status 401

- Else:
    - Code status 400
    - ``error`` JSON with errors

**Example**:

.. code-block:: javascript
    
    // POST Request to *your_bdn_host*/api/v1/courses/(?P<pk>[^/.]+)/edit_by_id/

    '/api/v1/courses/e0e433e9-477e-43a3-8e23-dfe2686202be/edit_by_id/',
    data={
        'title': 'test',
        'description': 'test',
        'external_link': 'http://example.com/',
    },
    HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
    HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'

-----------------------
Mark course as featured
-----------------------

Method ``mark_featured_by_id(self, request, pk=None)`` acccepting POST requests with inline id.

**Returns**

- If ok:
    - Code status 200

-Else if user is not creator of this course:
    - Code status 401

**Example**:

.. code-block:: javascript
    
    // POST Request to *your_bdn_host*/api/v1/courses/(?P<pk>[^/.]+)/mark_featured_by_id/

    '/api/v1/courses/e0e433e9-477e-43a3-8e23-dfe2686202be/mark_featured_by_id/',
    data={
    },
    HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
    HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'

-------------------
Delete course by id
-------------------

Method ``delete_by_id(self, request, pk=None)`` acccepting POST requests with inline id.

**Returns**

- If ok:
    - Code status 200

-Else if user is not creator of this course:
    - Code status 401

**Example**:

.. code-block:: javascript
    
    // POST Request to *your_bdn_host*/api/v1/courses/(?P<pk>[^/.]+)/delete_by_id/

    '/api/v1/courses/e0e433e9-477e-43a3-8e23-dfe2686202be/delete_by_id/',
    data={
    },
    HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
    HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
