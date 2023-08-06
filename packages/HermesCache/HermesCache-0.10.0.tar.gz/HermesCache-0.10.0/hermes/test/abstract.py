import asyncio
import threading
import time

from .. import Hermes, backend, test
from . import asynctest


class TestAbstract(test.TestCase):

  def setUp(self):
    self.testee  = Hermes(backend.AbstractBackend, ttl = 360)
    self.fixture = test.createFixture(self.testee)

    self.testee.clean()

  def testSimple(self):
    self.assertEqual(0, self.fixture.calls)

    self.assertEqual('ateb+ahpla', self.fixture.simple('alpha', b = 'beta'))
    self.assertEqual(1, self.fixture.calls)

    self.assertEqual('ateb+ahpla', self.fixture.simple('alpha', 'beta'))
    self.assertEqual(2, self.fixture.calls)

  @asynctest
  async def testAsyncSimple(self):
    self.assertEqual(0, self.fixture.calls)

    self.assertEqual('ateb+ahpla', await self.fixture.asimple('alpha', b = 'beta'))
    self.assertEqual(1, self.fixture.calls)

    self.assertEqual('ateb+ahpla', await self.fixture.asimple('alpha', 'beta'))
    self.assertEqual(2, self.fixture.calls)

  def testTagged(self):
    self.assertEqual(0,  self.fixture.calls)

    self.assertEqual('ae-hl', self.fixture.tagged('alpha', b = 'beta'))
    self.assertEqual(1,       self.fixture.calls)

    self.assertEqual('ae-hl', self.fixture.tagged('alpha', 'beta'))
    self.assertEqual(2,       self.fixture.calls)

  @asynctest
  async def testAsyncTagged(self):
    self.assertEqual(0,  self.fixture.calls)

    self.assertEqual('ae-hl', await self.fixture.atagged('alpha', b = 'beta'))
    self.assertEqual(1,       self.fixture.calls)

    self.assertEqual('ae-hl', await self.fixture.atagged('alpha', 'beta'))
    self.assertEqual(2,       self.fixture.calls)

  def testFunction(self):
    counter = dict(foo = 0, bar = 0)

    @self.testee
    def foo(a, b):
      counter['foo'] += 1
      return '{0}+{1}'.format(a, b)[::-1]

    key = lambda fn, *args, **kwargs: 'mk:{0}:{1}'.format(*args)

    @self.testee(tags = ('a', 'z'), key = key, ttl = 120)
    def bar(a, b):
      counter['bar'] += 1
      return '{0}-{1}'.format(a, b)[::2]


    self.assertEqual(0, counter['foo'])

    self.assertEqual('ateb+ahpla', foo('alpha', 'beta'))
    self.assertEqual(1, counter['foo'])

    self.assertEqual('ateb+ahpla', foo('alpha', 'beta'))
    self.assertEqual(2, counter['foo'])

    self.testee.clean()
    self.assertEqual(0, counter['bar'])

    self.assertEqual('apabt', bar('alpha', 'beta'))
    self.assertEqual(1,       counter['bar'])

    self.assertEqual('apabt', bar('alpha', 'beta'))
    self.assertEqual(2,       counter['bar'])

  @asynctest
  async def testAsyncFunction(self):
    counter = dict(foo = 0, bar = 0)

    @self.testee
    async def foo(a, b):
      await asyncio.sleep(0)
      counter['foo'] += 1
      return '{0}+{1}'.format(a, b)[::-1]

    key = lambda fn, *args, **kwargs: 'mk:{0}:{1}'.format(*args)

    @self.testee(tags = ('a', 'z'), key = key, ttl = 120)
    async def bar(a, b):
      await asyncio.sleep(0)
      counter['bar'] += 1
      return '{0}-{1}'.format(a, b)[::2]

    self.assertEqual(0, counter['foo'])

    self.assertEqual('ateb+ahpla', await foo('alpha', 'beta'))
    self.assertEqual(1, counter['foo'])

    self.assertEqual('ateb+ahpla', await foo('alpha', 'beta'))
    self.assertEqual(2, counter['foo'])

    self.testee.clean()
    self.assertEqual(0, counter['bar'])

    self.assertEqual('apabt', await bar('alpha', 'beta'))
    self.assertEqual(1,       counter['bar'])

    self.assertEqual('apabt', await bar('alpha', 'beta'))
    self.assertEqual(2,       counter['bar'])

  def testKey(self):
    self.assertEqual(0,  self.fixture.calls)

    self.assertEqual('apabt', self.fixture.key('alpha', 'beta'))
    self.assertEqual(1,       self.fixture.calls)

    self.assertEqual('apabt', self.fixture.key('alpha', 'beta'))
    self.assertEqual(2,       self.fixture.calls)

  @asynctest
  async def testAsyncKey(self):
    self.assertEqual(0,  self.fixture.calls)

    self.assertEqual('apabt', await self.fixture.akey('alpha', 'beta'))
    self.assertEqual(1,       self.fixture.calls)

    self.assertEqual('apabt', await self.fixture.akey('alpha', 'beta'))
    self.assertEqual(2,       self.fixture.calls)

  def testAll(self):
    self.assertEqual(0, self.fixture.calls)

    self.assertEqual({'a': ['beta'], 'b': {'b': 2}}, self.fixture.all({'alpha': ['beta']}, [2]))
    self.assertEqual(1, self.fixture.calls)

    self.assertEqual({'a': ['beta'], 'b': {'b': 2}}, self.fixture.all({'alpha': ['beta']}, [2]))
    self.assertEqual(2, self.fixture.calls)

  @asynctest
  async def testAsyncAll(self):
    self.assertEqual(0, self.fixture.calls)

    self.assertEqual(
      {'a': ['beta'], 'b': {'b': 2}}, await self.fixture.aall({'alpha': ['beta']}, [2])
    )
    self.assertEqual(1, self.fixture.calls)

    self.assertEqual(
      {'a': ['beta'], 'b': {'b': 2}}, await self.fixture.aall({'alpha': ['beta']}, [2])
    )
    self.assertEqual(2, self.fixture.calls)

  def testClean(self):
    self.assertEqual(0, self.fixture.calls)

    self.assertEqual('ateb+ahpla', self.fixture.simple('alpha', 'beta'))
    self.assertEqual('aldamg',     self.fixture.tagged('gamma', 'delta'))
    self.assertEqual(2,            self.fixture.calls)

    self.testee.clean()
    self.assertEqual(2, self.fixture.calls)

  @asynctest
  async def testAsyncClean(self):
    self.assertEqual(0, self.fixture.calls)

    self.assertEqual('ateb+ahpla', await self.fixture.asimple('alpha', 'beta'))
    self.assertEqual('aldamg',     await self.fixture.atagged('gamma', 'delta'))
    self.assertEqual(2,            self.fixture.calls)

    self.testee.clean()
    self.assertEqual(2, self.fixture.calls)

  def testCleanTagged(self):
    self.assertEqual(0, self.fixture.calls)

    self.assertEqual('ateb+ahpla', self.fixture.simple('alpha', 'beta'))
    self.assertEqual('aldamg',     self.fixture.tagged('gamma', 'delta'))
    self.assertEqual(2,            self.fixture.calls)

    self.testee.clean(('rock',))

    self.assertEqual('ateb+ahpla', self.fixture.simple('alpha', 'beta'))
    self.assertEqual('aldamg',     self.fixture.tagged('gamma', 'delta'))
    self.assertEqual(4,            self.fixture.calls)

    self.testee.clean(('rock', 'tree'))

    self.assertEqual('ateb+ahpla', self.fixture.simple('alpha', 'beta'))
    self.assertEqual('aldamg',     self.fixture.tagged('gamma', 'delta'))
    self.assertEqual(6,            self.fixture.calls)

    self.testee.clean()

    self.assertEqual(6,  self.fixture.calls)

  @asynctest
  async def testAsyncCleanTagged(self):
    self.assertEqual(0, self.fixture.calls)

    self.assertEqual('ateb+ahpla', await self.fixture.asimple('alpha', 'beta'))
    self.assertEqual('aldamg',     await self.fixture.atagged('gamma', 'delta'))
    self.assertEqual(2,            self.fixture.calls)

    self.testee.clean(('rock',))

    self.assertEqual('ateb+ahpla', await self.fixture.asimple('alpha', 'beta'))
    self.assertEqual('aldamg',     await self.fixture.atagged('gamma', 'delta'))
    self.assertEqual(4,            self.fixture.calls)

    self.testee.clean(('rock', 'tree'))

    self.assertEqual('ateb+ahpla', await self.fixture.asimple('alpha', 'beta'))
    self.assertEqual('aldamg',     await self.fixture.atagged('gamma', 'delta'))
    self.assertEqual(6,            self.fixture.calls)

    self.testee.clean()

    self.assertEqual(6, self.fixture.calls)

  def testNested(self):
    self.assertEqual('beta+alpha', self.fixture.nested('alpha', 'beta'))
    self.assertEqual(2, self.fixture.calls)

  @asynctest
  async def testAsyncNested(self):
    self.assertEqual('beta+alpha', await self.fixture.anested('alpha', 'beta'))
    self.assertEqual(2, self.fixture.calls)


class TestAbstractLock(test.TestCase):

  def setUp(self):
    self.testee = backend.AbstractLock('123')

  def testAcquire(self):
    for _ in range(2):
      try:
        self.assertTrue(self.testee.acquire(True))
        self.assertTrue(self.testee.acquire(False))
      finally:
        self.testee.release()

  def testRelease(self):
    for _ in range(2):
      try:
        self.assertTrue(self.testee.acquire(True))
        self.assertTrue(self.testee.acquire(False))
      finally:
        self.testee.release()

  def testWith(self):
    with self.testee:
      self.assertTrue(self.testee.acquire(False))

  def testConcurrent(self):
    log   = []
    check = threading.Lock()

    def target():
      with self.testee:
        locked = check.acquire(False)
        log.append(locked)
        time.sleep(0.05)
        if locked:
          check.release()
        time.sleep(0.05)

    threads = tuple(map(lambda i: threading.Thread(target = target), range(4)))
    tuple(map(threading.Thread.start, threads))
    tuple(map(threading.Thread.join,  threads))

    self.assertEqual([True, False, False, False], sorted(log, reverse = True))
