.. image:: https://img.shields.io/pypi/l/HermesCache.svg
   :target: https://spdx.org/licenses/LGPL-2.1+.html
   :alt: PyPI - License
.. image:: https://heptapod.host/saajns/hermes/badges/branch/default/pipeline.svg
   :target: https://heptapod.host/saajns/hermes/-/commits/branch/default
   :alt: Pipeline status
.. image:: https://heptapod.host/saajns/hermes/badges/branch/default/coverage.svg
   :target: https://heptapod.host/saajns/hermes/-/commits/branch/default
   :alt: Test code coverage
.. image:: https://badge.fury.io/py/HermesCache.svg
   :target: https://pypi.python.org/pypi/HermesCache
   :alt: PyPI
.. image:: https://readthedocs.org/projects/hermescache/badge/?version=latest
   :target: https://hermescache.readthedocs.io/en/latest/?badge=latest
   :alt: RTFD

***********
HermesCache
***********
Hermes is a Python caching library. It was designed to fulfil the following
requirements:

* Tag-based O(1) cache invalidation
* Dogpile effect (cache stampede) mitigation
* Support for multi-threaded, multi-process and multi-machine operation
* Cache compression
* Modular design (pluggable backends, compressors, serialisers, etc.)
* Simple yet flexible decorator API

Implemented backends: ``redis``, ``memcached``, ``inprocess``.

.. note::

   Hermes 0.10 provides experimental support for caching ``asyncio`` coroutines.

Installation
============
.. sourcecode::

   pip install HermesCache

For Redis and Memcached it has the following extra dependencies.

============================== =============================================
``HermesCache[redis]``         Pure Python Redis client
------------------------------ ---------------------------------------------
``HermesCache[redis-ext]``     Pure Python Redis client & C extension parser
------------------------------ ---------------------------------------------
``HermesCache[memcached]``     Pure Python Memcached client
============================== =============================================

Quickstart
==========
The following demonstrates the most of the package's API.

.. sourcecode:: python

   import hermes.backend.redis


   cache = hermes.Hermes(
     hermes.backend.redis.Backend,
     ttl = 600,
     host = 'localhost',
     db = 1,
   )

   @cache
   def foo(a, b):
     return a * b

   class Example:

     @cache(tags = ('math', 'power'), ttl = 1200)
     def bar(self, a, b):
       return a ** b

     @cache(tags = ('math', 'avg'), key = lambda fn, a, b: f'avg:{a}:{b}')
     def baz(self, a, b):
       return (a + b) / 2

   print(foo(2, 333))

   example = Example()
   print(example.bar(2, 10))
   print(example.baz(2, 10))

   foo.invalidate(2, 333)
   example.bar.invalidate(2, 10)
   example.baz.invalidate(2, 10)

   cache.clean(['math']) # invalidate entries tagged 'math'
   cache.clean()         # flush cache

.. note::

   The API encourages import-time instantiation of ``Hermes`` facade to allow
   decoration of existing classes and functions, to make caching transparent
   to them. The instantiation has no side-effects. Underlying backend
   connections are lazy.

   Moreover, if backend configuration is only available at runtime,
   ``Hermes.backend`` instance can be replaced at runtime.
