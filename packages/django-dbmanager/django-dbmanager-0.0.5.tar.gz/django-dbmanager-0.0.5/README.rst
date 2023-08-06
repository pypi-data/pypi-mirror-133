django-dbmanager
=================

django-dbmanager is a Django app to use for stockanalyser. For each question,
visitors can choose between a fixed number of answers.

Quick start
-----------

1. Add "dbmanager" to your INSTALLED_APPS setting like this

.. code::

    INSTALLED_APPS = [
        ...
        'dbmanager',
    ]

2. Add the namespace in urlpattern like this

.. code::

    urlpatterns = [
    ...
      path('dbmanager/', include('dbamanger.urls', namespace='dbmanager')),
    ]

3. Usage in the template

.. code::

    {% load dbmanager_custom_tags %}
    ...
    {% dbsetting %}

4. If you want to see appropriate html render, please use bootstrap 5.
