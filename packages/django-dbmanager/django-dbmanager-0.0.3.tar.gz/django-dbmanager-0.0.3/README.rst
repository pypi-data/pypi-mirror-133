#django-dbmanager

django-dbmanager is a Django app to use for stockanalyser. For each question,
visitors can choose between a fixed number of answers.

#Quick start

1. Add "dbmanager" to your INSTALLED_APPS setting like this::

```
    INSTALLED_APPS = [
        ...
        'dbmanager',
    ]
```

2.Usage in the template::
```
    {% load dbmanager_custom_tags %}
    ...
    {% dbsetting %}
```

3.If you want to see appropriate html render, please use bootstrap 5.
