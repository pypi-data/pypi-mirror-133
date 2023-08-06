import os
import telnetlib
import time
from typing import Dict

from .. import Hermes, test
from ..backend import memcached


class TestMemcached(test.BaseRemoteBackendTest):

  ttlDelta = 2

  def setUp(self):
    self.testee = Hermes(
      memcached.Backend,
      server = os.getenv('TEST_MEMCACHED_HOST', 'localhost'),
      ttl = 360,
    )
    self.addCleanup(self.testee.backend.client.close)

    super().setUp()

    # force flush memcached
    self.testee.backend.remove(getKeyTtlMapping().keys())

  def getSize(self):
    stats = self.testee.backend.client.stats()
    return int(stats[b'curr_items'])

  def assertEmptyBackend(self):
    # Can not use self.getSize because flushing works even worse in 1.4
    self.assertFalse(self.testee.backend.load(getKeyTtlMapping().keys()))

  def getKeyTtl(self, key: str):
    return max(-1, round(getKeyTtlMapping()[key]))

  def testLazyInit(self):
    server = test.FakeBackendServer()
    server.serve()

    addr = '{}:{}'.format(os.getenv('TEST_MEMCACHED_HOST', 'localhost'), server.port)
    Hermes(memcached.Backend, server = addr)

    server.close()
    self.assertEqual([], server.log)


class TestMemcachedLock(test.BaseRemoteBackendLockTest):

  ttlDelta = 2

  def setUp(self):
    self.cache = Hermes(memcached.Backend, server = os.getenv('TEST_MEMCACHED_HOST', 'localhost'))
    self.addCleanup(self.cache.backend.client.close)

    self.testee = memcached.Lock('123', self.cache.backend.client)

    super().setUp()

    # force flush memcached
    self.cache.backend.remove(getKeyTtlMapping().keys())

  def getKeyTtl(self, key: str):
    return max(-1, round(getKeyTtlMapping()[key]))


def getKeyTtlMapping() -> Dict[str, float]:
  '''
  Get dict that maps key to their TTL.

  What a poorly piece of software! Most of the early issues that happen
  during development are memcached issues. Most notable is that it
  won't flush damn keys. No matter how many times you call it to flush,
  or wait for clean state -- expired by flush call keys are just stale
  with expiry timestamp in past. Current version is 1.4.14.
  '''

  telnet = telnetlib.Telnet(os.getenv('TEST_MEMCACHED_HOST', 'localhost'), 11211)
  now = time.time()
  keys = {}
  try:
    telnet.write(b'stats items\n')
    slablines = telnet.read_until(b'END').split(b'\r\n')
    for slab in {int(s.decode().split(':')[1]) for s in slablines if s.startswith(b'STAT')}:
      telnet.write('stats cachedump {0} 0\n'.format(slab).encode())
      cachelines = telnet.read_until(b'END').split(b'\r\n')
      for line in cachelines:
        parts = line.decode().split(' ', 5)
        if len(parts) < 2:
          continue
        key = parts[1]
        ttl = int(parts[4]) - now
        keys[key] = ttl
  finally:
    telnet.close()

  return keys
