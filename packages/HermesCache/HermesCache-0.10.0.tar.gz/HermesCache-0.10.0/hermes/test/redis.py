import os

from .. import Hermes, test
from ..backend import redis


class TestRedis(test.BaseRemoteBackendTest):

  def setUp(self):
    self.testee = Hermes(
      redis.Backend,
      host = os.getenv('TEST_REDIS_HOST', 'localhost'),
      ttl = 360,
      lockconf = {'timeout': 120},
    )
    super().setUp()

  def getSize(self):
    return self.testee.backend.client.dbsize()

  def getKeyTtl(self, key: str):
    return self.testee.backend.client.ttl(key)

  def testLazyInit(self):
    server = test.FakeBackendServer()
    server.serve()

    Hermes(redis.Backend, port = server.port)

    server.close()
    self.assertEqual([], server.log)


class TestRedisLock(test.BaseRemoteBackendLockTest):

  def setUp(self):
    self.cache = Hermes(redis.Backend, host = os.getenv('TEST_REDIS_HOST', 'localhost'))
    self.testee = redis.Lock('123', self.cache.backend.client)
    super().setUp()

  def getKeyTtl(self, key: str):
    return self.cache.backend.client.ttl(key)
