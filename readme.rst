.. image:: https://travis-ci.com/ahmadsyafrudin/estimation-test.svg?branch=master
    :target: https://travis-ci.com/ahmadsyafrudin/estimation-test

PI FOR ESTIMATE(:WIP)
######################

this project is for testing purpose, using python version : 3.7

How to run locally
##################
Install `poetry
<https://python-poetry.org/docs/#installation>`_

install requirements:

.. code::

    pip install -r requirements.txt

adding new package requirement, add new line install_requires on setup.cfg and then run:

.. code::

    install_requires =
        django
        psycopg2-binary
        python-dateutil
        <<---Add-new-package-here--->>

.. code::

    poetry export -f requirements.txt --without-hashes > requirements.txt

run docker-compose for database:

.. code::

    docker-compose up

to run it in the background use options -d:

.. code::

    docker-compose up -d

migrate database

.. code::

    python manage.py migrate
    python manage.py loaddata test/fixtures/holiday

to run behave test:

.. code::

    behave test/features/delivery.feature

    behave test/features/pickup.feature

to run django app:

.. code::

    python manage.py runserver

to test the API we can use postman, estimation type delivery :

.. code-block::

    Host : localhost:8000/
    HTTP Method : POST
    Endpoint : "api/estimate/"
    Content-Type: "application/json"

    Request Body:

    {
        "estimationType": "delivery",
        "dateTime": "2019-05-10T13:00:00-07:00"
    }

Response:

.. code-block::

    Status : OK 200
    Content-Type: application/json

    {
        "order": "2019-05-10T13:00:00-07:00",
        "processing": "2019-05-13T13:00:00-07:00",
        "receive": "2019-05-14T13:00:00-07:00"
    }


example for return:

.. code-block::

    Host : localhost:8000/
    HTTP Method : POST
    Endpoint : "api/estimate/"
    Content-Type: "application/json"

    Request Body:

    {
        "estimationType": "return",
        "dateTime": "2019-05-10T13:00:00-07:00"
    }


Example Response:

.. code-block::

    Status : OK 200
    Content-Type: application/json

    {
        "return": "2019-05-10T13:00:00-07:00",
        "pickUp": "2019-05-11T13:00:00-07:00",
        "processedAndUnbooked": "2019-05-13T13:00:00-07:00"
    }


supported estimationType: "delivery", "return"

supported dateTime : ISO-8601

TODO:
-----
- input all holiday data on year 2019
- refactor unused function on helpers Estimate Object