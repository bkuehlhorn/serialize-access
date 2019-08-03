serialize_access
===============
.. image:: https://img.shields.io/travis/bkuehlhorn/dict_json/master.svg
   :target: https://travis-ci.org/bkuehlhorn/dict_json
.. image:: https://img.shields.io/pypi/v/dict_json.svg
   :target: https://pypi.python.org/pypi/dict_json
.. image:: https://img.shields.io/pypi/l/dict_json.svg
   :target: https://pypi.python.org/pypi/dict_json

A flexible utility for accessing nested dict and list objects in Python with single searialized key.

Introduction
------------
This Python package provide functions to access nested dict and list objects.
Provides a dynamic access to entries. Normal access is with several ``[]`` for
nested value.
Entries are accessed by string of delimited keys/indexes or list of keys/indexes.

* ``getValue(json_dict_list, key)`` returns value
* ``addValue(json_dict_list, key, value)`` adds value to key entry, additional dict/list are created to access entry
* ``getKeys(json_dict_list, serialize)`` returns list of serialized keys for each value in dict/list. serialize=True returns strings. False returns list

It also provides some key joining methods (reducer), and you can choose the reducer you want or even implement your own reducer. You can also choose to invert the resulting flat dict.

Documentation
-------------
serialize Access: getValue
````````````````````````````
.. code-block:: python

   def getValue(json_dict_list, key):
       """
       Key contains individual dict and list keys separated by ":"
       Returns final value from complex key. None is returned when partial key is not found

       :param key: string of keys with ":" DELIMITER
       :return: value of final key
       """

Examples
::::::::
.. code-block:: python

   In [1]: from serialize_access.serialize_access import getValue

   In [2]: normal_dict = {
      ...:     'a': '0',
      ...:     'b': {
      ...:         'a': '1.0',
      ...:         'b': '1.1',
      ...:     },
      ...:     'c': {
      ...:         'a': '2.0',
      ...:         'b': {
      ...:             'a': '2.1.0',
      ...:             'b': '2.1.1',
      ...:         },
      ...:     },
      ...: }

   In [ 3]: normal_dict['a'] # native python
   Out[ 3]: '0'
   In [ 4]: getValue(normal_dict, 'a')
   Out[ 4]: '0'

   In [ 5]: normal_dict['b']['a'] # native python
   Out[ 5]: '1.0'
   In [ 6]: getValue(normal_dict, 'b:a')
   Out[ 6]: '1.0'

   In [ 7]: normal_dict['c']['b']['b'] # native python
   Out[ 7]: '2.1.1'
   In [ 8]: getValue(normal_dict, 'c:b:b')
   Out[ 8]: '2.1.1'

   In [ 9]: normal_dict['c']['b']['b'] # native python
   Out[ 9]: '2.1.1'
   In [10]: getValue(normal_dict, ['c', 'b', 'b'])
   Out[10]: '2.1.1'

   In [2]: normal_list = [
      ...:     '0',
      ...:     [
      ...:         '1.0',
      ...:         '1.1',
      ...:     ],
      ...:     [
      ...:         '2.0',
      ...:         [
      ...:             '2.1.0',
      ...:             '2.1.1',
      ...:         ],
      ...:     ],
      ...: }

   In [ 3]: normal_dict['0'] # native python
   Out[ 3]: '0'
   In [ 4]: getValue(normal_dict, '0')
   Out[ 4]: '0'

   In [ 5]: normal_dict['1']['0'] # native python
   Out[ 5]: '1.0'
   In [ 6]: getValue(normal_dict, '1:0')
   Out[ 6]: '1.0'

   In [ 7]: normal_list[2][1][1]  # native python
   Out[ 7]: '2.1.1'
   In [ 8]: getValue(normal_dict, '2:1:1')
   Out[ 8]: '2.1.1'

   In [ 9]: normal_list[2][1][1]  # native python
   Out[ 9]: '2.1.1'
   In [10]: getValue(normal_dict, [2, 1, 1])
   Out[10]: '2.1.1'

serialize Access: setValue
````````````````````````````
.. code-block:: python

   def setValue(json_dict_list, key, value):
       """
    Find last key in json_dict_list from key string
    Add [] for missing keys when next is int
    add MyDict() for missing keys when next is not int

    verify key:
        is int: make list
        is list: make copy
        is other: split by delimiter

    verify json_dict_list:
        is list or dict:
            set myDict
        is other:

    pop last_key

    for each key
        if can walk: walk to next myDict
        else: add new node for key

    if myDict is (dict or list):
    else: add dict or list

    myDict[last_key] = value

    :param key: string of keys with ":" DELIMITER
    :param value: value for last key
    :return: None
       """

Examples
::::::::
.. code-block:: python

   In [1]: from serialize_access.serialize_access import setValue

   In [2]: normal_dict = {
      ...:     'a': '0',
      ...:     'b': {
      ...:         'a': '1.0',
      ...:         'b': '1.1',
      ...:     },
      ...:     'c': {
      ...:         'a': '2.0',
      ...:         'b': {
      ...:             'a': '2.1.0',
      ...:             'b': '2.1.1',
      ...:         },
      ...:     },
      ...: }

   In [3]: setValue(normal_dict, 'a', 'newvalue')
   In [4]: normal_dict['a']
   Out[4]: 'newvalue'


   In [5]: setValue(normal_dict, 'b:a', 'newvalue')
   In [6]: normal_dict['b']['a']
   Out[6]: 'newvalue'

   In [7]: setValue(normal_dict, 'c:c:b', 'newvalue newnode')
   In [8]: normal_dict['c']['c']['b']
   Out[8]: 'newvalue newnode'

serialize Access: getKeys
````````````````````````````
.. code-block:: python

   def getKeys(json_dict_list, serialize=True):
       """
       get unique string of keys to values in response dict
       list use 0 for entry

       Add support to return keys as list

       :return: list of all key string to access elements
       """

Examples
::::::::
.. code-block:: python

   In [1]: from serialize_access.serialize_access import getKeys

   In [2]: normal_dict = {
      ...:    'a': '0',
      ...:    'b': {
      ...:        'a': '1.0',
      ...:        'b': '1.1', },
      ...:    'c': {
      ...:        'a': '2.0',
      ...:        'b': {
      ...:            'a': '2.1.0',
      ...:            'b': '2.1.1', },
      ...:    },
      ...:}

   In [3]: getKeys(normal_dict)
   Out[3]: ['a', 'b:a', 'b:b', 'c:a', 'c:b:a', 'c:b:b']

   In [4]: getKeys(normal_dict, serialize=False)
   Out[4]: [['a'], ['b', 'a'], ['b', 'b'], ['c', 'a'], ['c', 'b', 'a'], ['c', 'b', 'b']]
