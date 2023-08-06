from setuptools import setup


setup(
  name         = 'HermesCache',
  version      = '0.10.0',
  author       = 'saaj',
  author_email = 'mail@saaj.me',
  packages     = ['hermes', 'hermes.backend', 'hermes.test'],
  url          = 'https://heptapod.host/saajns/hermes',
  project_urls = {
    'Source Code'   : 'https://heptapod.host/saajns/hermes',
    'Documentation' : 'https://hermescache.readthedocs.io/',
  },
  license     = 'LGPL-2.1+',
  description = (
    'Python caching library with tag-based invalidation and dogpile effect prevention'
  ),
  long_description = open('README.rst', 'rb').read().decode('utf-8'),
  platforms        = ['Any'],
  python_requires  = '>= 3',
  keywords         = 'python cache tagging redis memcached',
  classifiers      = [
    'Topic :: Software Development :: Libraries',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Intended Audience :: Developers',
  ],
  extras_require = {
    'redis'     : ['redis'],
    'redis-ext' : ['redis', 'hiredis'],
    'memcached' : ['pymemcache'],
  },
)
