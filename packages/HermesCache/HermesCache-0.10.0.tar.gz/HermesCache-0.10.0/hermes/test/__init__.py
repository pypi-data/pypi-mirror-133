import asyncio
import inspect
import socket
import threading
import time
import unittest

from .. import Hermes, backend


def load_tests(loader, tests, pattern):
  from . import abstract, facade, inprocess, memcached, redis  # noqa: F401

  suite = unittest.TestSuite()
  for m in filter(inspect.ismodule, locals().values()):
    suite.addTests(loader.loadTestsFromModule(m))

  return suite


class TestCase(unittest.TestCase):

  testee = None
  fixture = None

  def _arghash(self, *args, **kwargs):
    '''
    Not very neat as it penetrates into an implementation detail,
    though otherwise it'll be harder to make assertion on keys.
    '''

    arguments = args, tuple(sorted(kwargs.items()))
    return self.testee.mangler.hash(self.testee.mangler.dumps(arguments))


def createFixture(cache):  # noqa: C901

  class Fixture:

    calls = 0

    @cache
    def simple(self, a, b):
      '''Here be dragons... seriously just a docstring test.'''

      self.calls += 1
      return '{0}+{1}'.format(a, b)[::-1]

    @cache
    def nested(self, a, b):
      self.calls += 1
      return self.simple(b, a)[::-1]

    @cache(tags = ('rock', 'tree'))
    def tagged(self, a, b):
      self.calls += 1
      return '{0}-{1}'.format(a, b)[::-2]

    @cache(tags = ('rock', 'ice'))
    def tagged2(self, a, b):
      self.calls += 1
      return '{0}%{1}'.format(a, b)[::-2]

    @cache(tags = ('ash', 'stone'), key = lambda fn, a, b: f'mykey:{a}:{b}')
    def key(self, a, b):
      self.calls += 1
      return '{0}*{1}'.format(a, b)[::2]

    @cache(
      tags = ('a', 'z'),
      key = lambda fn, *a: 'mk:{0}:{1}'.format(*a).replace(' ', ''),
      ttl = 1200,
    )
    def all(self, a, b):
      self.calls += 1
      return {'a': a['alpha'], 'b': {'b': b[0]}}

    @cache
    async def asimple(self, a, b):
      await asyncio.sleep(0)
      self.calls += 1
      return '{0}+{1}'.format(a, b)[::-1]

    @cache
    async def anested(self, a, b):
      self.calls += 1
      return (await self.asimple(b, a))[::-1]

    @cache(tags = ('rock', 'tree'))
    async def atagged(self, a, b):
      await asyncio.sleep(0)
      self.calls += 1
      return '{0}-{1}'.format(a, b)[::-2]

    @cache(tags = ('rock', 'ice'))
    async def atagged2(self, a, b):
      await asyncio.sleep(0)
      self.calls += 1
      return '{0}%{1}'.format(a, b)[::-2]

    @cache(tags = ('ash', 'stone'), key = lambda fn, a, b: f'mykey:{a}:{b}')
    async def akey(self, a, b):
      await asyncio.sleep(0)
      self.calls += 1
      return '{0}*{1}'.format(a, b)[::2]

    @cache(
      tags = ('a', 'z'),
      key = lambda fn, *a: 'mk:{0}:{1}'.format(*a).replace(' ', ''),
      ttl = 1200,
    )
    async def aall(self, a, b):
      await asyncio.sleep(0)
      self.calls += 1
      return {'a': a['alpha'], 'b': {'b': b[0]}}

  return Fixture()


def asynctest(coro):
  assert inspect.iscoroutinefunction(coro)

  def wrapper(self):
    return asyncio.run(coro(self))

  return wrapper


class FakeBackendServer:

  port = None
  '''Fake server port.'''

  log = None
  '''Activity log.'''

  thread = None
  '''Server connection-accepting thread.'''

  closing = None
  '''Whether connection is closing.'''

  def __init__(self):
    self.log = []

  def serve(self):
    self.closing = False

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('', 0))
    serverSocket.listen(1)

    self.port = serverSocket.getsockname()[1]

    self.thread = threading.Thread(target = self.target, args = (serverSocket,))
    self.thread.start()

  def close(self):
    self.closing = True

    clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSock.connect(('localhost', self.port))

    clientSock.close()

    self.thread.join()

  def target(self, serverSocket):
    clientSocket, _ = serverSocket.accept()

    if not self.closing:
      self.log.append('connected')

    try:
      chunk = clientSocket.recv(1024)
      if not self.closing:
        if not chunk:
          self.log.append('closed')
        else:
          self.log.append('received {}'.format(chunk))
    finally:
      clientSocket.close()
      serverSocket.close()


class BaseRemoteBackendTest(TestCase):

  ttlDelta = 0

  def setUp(self):
    '''``testee`` is expected to be created in override.'''

    self.fixture = createFixture(self.testee)

    self.testee.clean()
    self.addCleanup(self.testee.clean)

  def getSize(self) -> int:
    raise NotImplementedError

  def getKeyTtl(self, key: str) -> int:
    raise NotImplementedError

  def assertEmptyBackend(self):
    self.assertEqual(0, self.getSize())

  def testSimple(self):
    self.assertEqual(0, self.fixture.calls)
    self.assertEmptyBackend()

    key = 'cache:entry:hermes.test:Fixture:simple:' + self._arghash('alpha', b = 'beta')
    for _ in range(4):
      self.assertEqual('ateb+ahpla', self.fixture.simple('alpha', b = 'beta'))
      self.assertEqual(1, self.fixture.calls)
      self.assertEqual(1, self.getSize())

      self.assertAlmostEqual(360, self.getKeyTtl(key), delta = self.ttlDelta)
      self.assertEqual(
        'ateb+ahpla', self.testee.mangler.loads(self.testee.backend.client.get(key))
      )

    self.fixture.simple.invalidate('alpha', b = 'beta')
    self.assertEmptyBackend()


    expected = "]}'ammag'{[+}]'ateb'[ :'ahpla'{"
    key      = 'cache:entry:hermes.test:Fixture:simple:{}'.format(
      self._arghash({'alpha': ['beta']}, [{'gamma'}]))
    for _ in range(4):
      self.assertEqual(expected, self.fixture.simple({'alpha': ['beta']}, [{'gamma'}]))

      self.assertEqual(2, self.fixture.calls)
      self.assertEqual(1, self.getSize())

      self.assertAlmostEqual(360, self.getKeyTtl(key), delta = self.ttlDelta)

      self.assertEqual(expected, self.testee.mangler.loads(self.testee.backend.client.get(key)))

  @asynctest
  async def testAsyncSimple(self):
    self.assertEqual(0, self.fixture.calls)
    self.assertEmptyBackend()

    key = 'cache:entry:hermes.test:Fixture:asimple:' + self._arghash('alpha', b = 'beta')
    for _ in range(4):
      self.assertEqual('ateb+ahpla', await self.fixture.asimple('alpha', b = 'beta'))
      self.assertEqual(1, self.fixture.calls)
      self.assertEqual(1, self.getSize())

      self.assertAlmostEqual(360, self.getKeyTtl(key), delta = self.ttlDelta)
      self.assertEqual(
        'ateb+ahpla', self.testee.mangler.loads(self.testee.backend.client.get(key))
      )

    await self.fixture.asimple.invalidate('alpha', b = 'beta')
    self.assertEmptyBackend()


    expected = "]}'ammag'{[+}]'ateb'[ :'ahpla'{"
    key      = 'cache:entry:hermes.test:Fixture:asimple:{}'.format(
      self._arghash({'alpha': ['beta']}, [{'gamma'}]))
    for _ in range(4):
      self.assertEqual(expected, await self.fixture.asimple({'alpha': ['beta']}, [{'gamma'}]))

      self.assertEqual(2, self.fixture.calls)
      self.assertEqual(1, self.getSize())

      self.assertAlmostEqual(360, self.getKeyTtl(key), delta = self.ttlDelta)

      self.assertEqual(expected, self.testee.mangler.loads(self.testee.backend.client.get(key)))

  def testTagged(self):
    self.assertEqual(0, self.fixture.calls)
    self.assertEmptyBackend()

    for _ in range(4):
      self.assertEqual('ae-hl', self.fixture.tagged('alpha', b = 'beta'))
      self.assertEqual(1,       self.fixture.calls)
      self.assertEqual(3,       self.getSize())

      self.assertEqual(-1,  self.getKeyTtl('cache:tag:rock'))
      self.assertEqual(-1,  self.getKeyTtl('cache:tag:tree'))
      rockTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:rock'))
      treeTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:tree'))
      self.assertFalse(rockTag == treeTag)
      self.assertEqual(22, len(rockTag))
      self.assertEqual(22, len(treeTag))

      argHash = self._arghash('alpha', b = 'beta')
      tagHash = self.testee.mangler.hashTags(dict(tree = treeTag, rock = rockTag))
      key     = 'cache:entry:hermes.test:Fixture:tagged:{0}:{1}'.format(argHash, tagHash)
      self.assertAlmostEqual(360, self.getKeyTtl(key), delta = self.ttlDelta)
      self.assertEqual('ae-hl', self.testee.mangler.loads(self.testee.backend.client.get(key)))

    self.fixture.tagged.invalidate('alpha', b = 'beta')

    self.assertEqual(2, self.getSize())

    rockTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:rock'))
    treeTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:tree'))
    self.assertNotEqual(rockTag, treeTag)
    self.assertEqual(22, len(rockTag))
    self.assertEqual(22, len(treeTag))

    for _ in range(4):
      self.assertEqual('ae-hl', self.fixture.tagged('alpha', 'beta'))
      self.assertEqual('ae%hl', self.fixture.tagged2('alpha', 'beta'))
      self.assertEqual(3, self.fixture.calls)

      self.assertEqual(5, self.getSize())
      self.assertEqual(
        rockTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:rock'))
      )
      self.assertEqual(
        treeTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:tree'))
      )
      self.assertEqual(
        22, len(self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:ice')))
      )

    self.testee.clean(['rock'])

    self.assertEqual(4, self.getSize())
    self.assertIsNone(self.testee.backend.client.get('cache:tag:rock'))
    iceTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:ice'))

    for _ in range(4):
      self.assertEqual('ae-hl', self.fixture.tagged('alpha', 'beta'))
      self.assertEqual('ae%hl', self.fixture.tagged2('alpha', 'beta'))
      self.assertEqual(5, self.fixture.calls)

      size = self.getSize()
      self.assertEqual(7, size, 'has new and old entries for tagged and tagged 2 + 3 tags')
      self.assertEqual(
        treeTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:tree'))
      )
      self.assertEqual(
        iceTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:ice'))
      )
      self.assertEqual(
        22, len(self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:rock')))
      )
      self.assertNotEqual(
        rockTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:rock'))
      )

  @asynctest
  async def testAsyncTagged(self):
    self.assertEqual(0, self.fixture.calls)
    self.assertEmptyBackend()

    for _ in range(4):
      self.assertEqual('ae-hl', await self.fixture.atagged('alpha', b = 'beta'))
      self.assertEqual(1,       self.fixture.calls)
      self.assertEqual(3,       self.getSize())

      self.assertEqual(-1,  self.getKeyTtl('cache:tag:rock'))
      self.assertEqual(-1,  self.getKeyTtl('cache:tag:tree'))
      rockTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:rock'))
      treeTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:tree'))
      self.assertFalse(rockTag == treeTag)
      self.assertEqual(22, len(rockTag))
      self.assertEqual(22, len(treeTag))

      argHash = self._arghash('alpha', b = 'beta')
      tagHash = self.testee.mangler.hashTags(dict(tree = treeTag, rock = rockTag))
      key     = 'cache:entry:hermes.test:Fixture:atagged:{0}:{1}'.format(argHash, tagHash)
      self.assertAlmostEqual(360, self.getKeyTtl(key), delta = self.ttlDelta)
      self.assertEqual('ae-hl', self.testee.mangler.loads(self.testee.backend.client.get(key)))

    await self.fixture.atagged.invalidate('alpha', b = 'beta')

    self.assertEqual(2, self.getSize())

    rockTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:rock'))
    treeTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:tree'))
    self.assertNotEqual(rockTag, treeTag)
    self.assertEqual(22, len(rockTag))
    self.assertEqual(22, len(treeTag))

    for _ in range(4):
      self.assertEqual('ae-hl', await self.fixture.atagged('alpha', 'beta'))
      self.assertEqual('ae%hl', await self.fixture.atagged2('alpha', 'beta'))
      self.assertEqual(3, self.fixture.calls)

      self.assertEqual(5, self.getSize())
      self.assertEqual(
        rockTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:rock'))
      )
      self.assertEqual(
        treeTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:tree'))
      )
      self.assertEqual(
        22, len(self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:ice')))
      )

    self.testee.clean(['rock'])

    self.assertEqual(4, self.getSize())
    self.assertIsNone(self.testee.backend.client.get('cache:tag:rock'))
    iceTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:ice'))

    for _ in range(4):
      self.assertEqual('ae-hl', self.fixture.tagged('alpha', 'beta'))
      self.assertEqual('ae%hl', self.fixture.tagged2('alpha', 'beta'))
      self.assertEqual(5, self.fixture.calls)

      size = self.getSize()
      self.assertEqual(7, size, 'has new and old entries for tagged and tagged 2 + 3 tags')
      self.assertEqual(
        treeTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:tree'))
      )
      self.assertEqual(
        iceTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:ice'))
      )
      self.assertEqual(
        22, len(self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:rock')))
      )
      self.assertNotEqual(
        rockTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:rock'))
      )

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
    self.assertEmptyBackend()

    key = 'cache:entry:hermes.test:foo:' + self._arghash('alpha', 'beta')
    for _ in range(4):
      self.assertEqual('ateb+ahpla', foo('alpha', 'beta'))

      self.assertEqual(1, counter['foo'])
      self.assertEqual(1, self.getSize())

      self.assertAlmostEqual(360, self.getKeyTtl(key), delta = self.ttlDelta)
      self.assertEqual(
        'ateb+ahpla', self.testee.mangler.loads(self.testee.backend.client.get(key))
      )

    foo.invalidate('alpha', 'beta')
    self.assertFalse(self.testee.backend.client.get(key))
    self.assertEmptyBackend()


    self.assertEqual(0, counter['bar'])
    self.assertEmptyBackend()

    for _ in range(4):
      self.assertEqual('apabt', bar('alpha', 'beta'))
      self.assertEqual(1,       counter['bar'])
      self.assertEqual(3,       self.getSize())

      self.assertEqual(-1, self.getKeyTtl('cache:tag:a'))
      self.assertEqual(-1, self.getKeyTtl('cache:tag:z'))

      aTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:a'))
      zTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:z'))
      self.assertFalse(aTag == zTag)
      self.assertEqual(22, len(aTag))
      self.assertEqual(22, len(zTag))

      tagHash = self.testee.mangler.hashTags(dict(a = aTag, z = zTag))
      key     = 'mk:alpha:beta:' + tagHash
      self.assertAlmostEqual(120, self.getKeyTtl(key), delta = self.ttlDelta)
      self.assertEqual('apabt', self.testee.mangler.loads(self.testee.backend.client.get(key)))

    bar.invalidate('alpha', 'beta')
    self.assertEqual(1,  counter['foo'])
    self.assertIsNone(self.testee.backend.client.get(key))
    self.assertEqual(2, self.getSize())

    self.assertEqual('apabt', bar('alpha', 'beta'))
    self.assertEqual(2, counter['bar'])
    self.assertEqual(3, self.getSize())

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
      counter['bar'] += 1
      return '{0}-{1}'.format(a, b)[::2]


    self.assertEqual(0, counter['foo'])
    self.assertEmptyBackend()

    key = 'cache:entry:hermes.test:foo:' + self._arghash('alpha', 'beta')
    for _ in range(4):
      self.assertEqual('ateb+ahpla', await foo('alpha', 'beta'))

      self.assertEqual(1, counter['foo'])
      self.assertEqual(1, self.getSize())

      self.assertAlmostEqual(360, self.getKeyTtl(key), delta = self.ttlDelta)
      self.assertEqual(
        'ateb+ahpla', self.testee.mangler.loads(self.testee.backend.client.get(key))
      )

    await foo.invalidate('alpha', 'beta')
    self.assertFalse(self.testee.backend.client.get(key))
    self.assertEmptyBackend()


    self.assertEqual(0, counter['bar'])
    self.assertEmptyBackend()

    for _ in range(4):
      self.assertEqual('apabt', await bar('alpha', 'beta'))
      self.assertEqual(1, counter['bar'])
      self.assertEqual(3, self.getSize())

      self.assertEqual(-1, self.getKeyTtl('cache:tag:a'))
      self.assertEqual(-1, self.getKeyTtl('cache:tag:z'))

      aTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:a'))
      zTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:z'))
      self.assertFalse(aTag == zTag)
      self.assertEqual(22, len(aTag))
      self.assertEqual(22, len(zTag))

      tagHash = self.testee.mangler.hashTags(dict(a = aTag, z = zTag))
      key     = 'mk:alpha:beta:' + tagHash
      self.assertAlmostEqual(120, self.getKeyTtl(key), delta = self.ttlDelta)
      self.assertEqual('apabt', self.testee.mangler.loads(self.testee.backend.client.get(key)))

    await bar.invalidate('alpha', 'beta')
    self.assertEqual(1,  counter['foo'])
    self.assertIsNone(self.testee.backend.client.get(key))
    self.assertEqual(2, self.getSize())

    self.assertEqual('apabt', await bar('alpha', 'beta'))
    self.assertEqual(2, counter['bar'])
    self.assertEqual(3, self.getSize())

  def testKey(self):
    self.assertEqual(0, self.fixture.calls)
    self.assertEmptyBackend()

    for _ in range(4):
      self.assertEqual('apabt', self.fixture.key('alpha', 'beta'))
      self.assertEqual(1,       self.fixture.calls)
      self.assertEqual(3,       self.getSize())

      self.assertEqual(-1,  self.getKeyTtl('cache:tag:ash'))
      self.assertEqual(-1,  self.getKeyTtl('cache:tag:stone'))
      ashTag   = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:ash'))
      stoneTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:stone'))
      self.assertFalse(ashTag == stoneTag)
      self.assertEqual(22, len(ashTag))
      self.assertEqual(22, len(stoneTag))

      tagHash = self.testee.mangler.hashTags(dict(ash = ashTag, stone = stoneTag))
      key     = 'mykey:alpha:beta:' + tagHash
      self.assertAlmostEqual(360, self.getKeyTtl(key), delta = self.ttlDelta)
      self.assertEqual('apabt', self.testee.mangler.loads(self.testee.backend.client.get(key)))

    self.fixture.key.invalidate('alpha', 'beta')

    self.assertIsNone(self.testee.backend.client.get(key))
    self.assertEqual(2, self.getSize())

    self.assertEqual(
      ashTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:ash'))
    )
    self.assertEqual(
      stoneTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:stone'))
    )

  @asynctest
  async def testAsyncKey(self):
    self.assertEqual(0, self.fixture.calls)
    self.assertEmptyBackend()

    for _ in range(4):
      self.assertEqual('apabt', await self.fixture.akey('alpha', 'beta'))
      self.assertEqual(1,       self.fixture.calls)
      self.assertEqual(3,       self.getSize())

      self.assertEqual(-1,  self.getKeyTtl('cache:tag:ash'))
      self.assertEqual(-1,  self.getKeyTtl('cache:tag:stone'))
      ashTag   = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:ash'))
      stoneTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:stone'))
      self.assertFalse(ashTag == stoneTag)
      self.assertEqual(22, len(ashTag))
      self.assertEqual(22, len(stoneTag))

      tagHash = self.testee.mangler.hashTags(dict(ash = ashTag, stone = stoneTag))
      key     = 'mykey:alpha:beta:' + tagHash
      self.assertAlmostEqual(360, self.getKeyTtl(key), delta = self.ttlDelta)
      self.assertEqual('apabt', self.testee.mangler.loads(self.testee.backend.client.get(key)))

    await self.fixture.akey.invalidate('alpha', 'beta')

    self.assertIsNone(self.testee.backend.client.get(key))
    self.assertEqual(2, self.getSize())

    self.assertEqual(
      ashTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:ash'))
    )
    self.assertEqual(
      stoneTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:stone'))
    )

  def testAll(self):
    self.assertEqual(0, self.fixture.calls)
    self.assertEmptyBackend()
    for _ in range(4):
      self.assertEqual({'a': 1, 'b': {'b': 'beta'}}, self.fixture.all({'alpha': 1}, ['beta']))
      self.assertEqual(1, self.fixture.calls)
      self.assertEqual(3, self.getSize())

      self.assertEqual(-1, self.getKeyTtl('cache:tag:a'))
      self.assertEqual(-1, self.getKeyTtl('cache:tag:z'))

      aTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:a'))
      zTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:z'))
      self.assertFalse(aTag == zTag)
      self.assertEqual(22, len(aTag))
      self.assertEqual(22, len(zTag))

      tagHash = self.testee.mangler.hashTags(dict(a = aTag, z = zTag))
      key = "mk:{'alpha':1}:['beta']:" + tagHash
      self.assertAlmostEqual(1200, self.getKeyTtl(key), delta = self.ttlDelta)
      self.assertEqual(
        {'a': 1, 'b': {'b': 'beta'}},
        self.testee.mangler.loads(self.testee.backend.client.get(key)),
      )

    self.fixture.all.invalidate({'alpha': 1}, ['beta'])

    self.assertEqual(2, self.getSize())
    self.assertEqual(
      aTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:a'))
    )
    self.assertEqual(
      zTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:z'))

    )

  @asynctest
  async def testAsyncAll(self):
    self.assertEqual(0, self.fixture.calls)
    self.assertEmptyBackend()
    for _ in range(4):
      self.assertEqual(
        {'a': 1, 'b': {'b': 'beta'}}, await self.fixture.aall({'alpha': 1}, ['beta'])
      )
      self.assertEqual(1, self.fixture.calls)
      self.assertEqual(3, self.getSize())

      self.assertEqual(-1, self.getKeyTtl('cache:tag:a'))
      self.assertEqual(-1, self.getKeyTtl('cache:tag:z'))

      aTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:a'))
      zTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:z'))
      self.assertFalse(aTag == zTag)
      self.assertEqual(22, len(aTag))
      self.assertEqual(22, len(zTag))

      tagHash = self.testee.mangler.hashTags(dict(a = aTag, z = zTag))
      key = "mk:{'alpha':1}:['beta']:" + tagHash
      self.assertAlmostEqual(1200, self.getKeyTtl(key), delta = self.ttlDelta)
      self.assertEqual(
        {'a': 1, 'b': {'b': 'beta'}},
        self.testee.mangler.loads(self.testee.backend.client.get(key)),
      )

    await self.fixture.aall.invalidate({'alpha': 1}, ['beta'])

    self.assertEqual(2, self.getSize())
    self.assertEqual(
      aTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:a'))
    )
    self.assertEqual(
      zTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:z'))
    )

  def testClean(self):
    self.assertEqual(0, self.fixture.calls)
    self.assertEmptyBackend()

    self.assertEqual('ateb+ahpla', self.fixture.simple('alpha', 'beta'))
    self.assertEqual('aldamg',     self.fixture.tagged('gamma', 'delta'))
    self.assertEqual(2,            self.fixture.calls)
    self.assertEqual(4,            self.getSize())

    self.testee.clean()

    self.assertEqual(2, self.fixture.calls)
    self.assertEmptyBackend()

  @asynctest
  async def testAsyncClean(self):
    self.assertEqual(0, self.fixture.calls)
    self.assertEmptyBackend()

    self.assertEqual('ateb+ahpla', await self.fixture.asimple('alpha', 'beta'))
    self.assertEqual('aldamg',     await self.fixture.atagged('gamma', 'delta'))
    self.assertEqual(2,            self.fixture.calls)
    self.assertEqual(4,            self.getSize())

    self.testee.clean()

    self.assertEqual(2, self.fixture.calls)
    self.assertEmptyBackend()

  def testCleanTagged(self):
    self.assertEqual(0, self.fixture.calls)
    self.assertEmptyBackend()

    self.assertEqual('ateb+ahpla', self.fixture.simple('alpha', 'beta'))
    self.assertEqual('aldamg',     self.fixture.tagged('gamma', 'delta'))
    self.assertEqual(2,            self.fixture.calls)
    self.assertEqual(4,            self.getSize())

    simpleKey = 'cache:entry:hermes.test:Fixture:simple:' + self._arghash('alpha', 'beta')
    self.assertEqual(
      'ateb+ahpla', self.testee.mangler.loads(self.testee.backend.client.get(simpleKey))
    )

    rockTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:rock'))
    treeTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:tree'))
    self.assertFalse(rockTag == treeTag)
    self.assertEqual(22, len(rockTag))
    self.assertEqual(22, len(treeTag))

    argHash   = self._arghash('gamma', 'delta')
    tagHash   = self.testee.mangler.hashTags(dict(tree = treeTag, rock = rockTag))
    taggedKey = 'cache:entry:hermes.test:Fixture:tagged:{0}:{1}'.format(argHash, tagHash)
    self.assertEqual(
      'aldamg', self.testee.mangler.loads(self.testee.backend.client.get(taggedKey))
    )


    self.testee.clean(('rock',))
    self.assertEqual(3, self.getSize())

    self.assertEqual(
      'ateb+ahpla', self.testee.mangler.loads(self.testee.backend.client.get(simpleKey))
    )

    self.assertIsNone(self.testee.backend.client.get('cache:tag:rock'))
    self.assertEqual(
      treeTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:tree'))
    )

    # stale still accessible, though only directly
    self.assertEqual(
      'aldamg', self.testee.mangler.loads(self.testee.backend.client.get(taggedKey))
    )


    self.assertEqual('ateb+ahpla', self.fixture.simple('alpha', 'beta'))
    self.assertEqual('aldamg',     self.fixture.tagged('gamma', 'delta'))
    self.assertEqual(3,            self.fixture.calls)
    self.assertEqual(5,            self.getSize(), '+1 old tagged entry')

    self.assertEqual(
      'ateb+ahpla', self.testee.mangler.loads(self.testee.backend.client.get(simpleKey))
    )

    self.assertNotEqual(
      rockTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:rock'))
    )
    rockTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:rock'))
    self.assertFalse(rockTag == treeTag)
    self.assertEqual(22, len(rockTag))
    self.assertEqual(
      treeTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:tree'))
    )

    # stale still accessible, though only directly
    self.assertEqual(
      'aldamg', self.testee.mangler.loads(self.testee.backend.client.get(taggedKey))
    )

    argHash   = self._arghash('gamma', 'delta')
    tagHash   = self.testee.mangler.hashTags(dict(tree = treeTag, rock = rockTag))
    taggedKey = 'cache:entry:hermes.test:Fixture:tagged:{0}:{1}'.format(argHash, tagHash)
    self.assertEqual(
      'aldamg', self.testee.mangler.loads(self.testee.backend.client.get(taggedKey))
    )


    self.testee.clean(('rock', 'tree'))
    self.assertEqual(3, self.getSize(), 'simaple, new tagged and old tagged')

    self.assertEqual(
      'ateb+ahpla', self.testee.mangler.loads(self.testee.backend.client.get(simpleKey))
    )

    # new stale is accessible, though only directly
    self.assertEqual(
      'aldamg', self.testee.mangler.loads(self.testee.backend.client.get(taggedKey))
    )


    self.assertEqual('ateb+ahpla', self.fixture.simple('alpha', 'beta'))
    self.assertEqual('aldamg',     self.fixture.tagged('gamma', 'delta'))
    self.assertEqual(4,            self.fixture.calls)
    self.assertEqual(6,            self.getSize(), '+2 old tagged entries')

    self.assertEqual(
      'ateb+ahpla', self.testee.mangler.loads(self.testee.backend.client.get(simpleKey))
    )

    # new stale still accessible, though only directly
    self.assertEqual(
      'aldamg', self.testee.mangler.loads(self.testee.backend.client.get(taggedKey))
    )

    self.assertNotEqual(
      rockTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:rock'))
    )
    self.assertNotEqual(
      treeTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:tree'))
    )

    rockTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:rock'))
    treeTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:tree'))
    self.assertFalse(rockTag == treeTag)
    self.assertEqual(22, len(rockTag))
    self.assertEqual(22, len(treeTag))

    argHash   = self._arghash('gamma', 'delta')
    tagHash   = self.testee.mangler.hashTags(dict(tree = treeTag, rock = rockTag))
    taggedKey = 'cache:entry:hermes.test:Fixture:tagged:{0}:{1}'.format(argHash, tagHash)
    self.assertEqual(
      'aldamg', self.testee.mangler.loads(self.testee.backend.client.get(taggedKey))
    )


    self.testee.clean(('rock', 'tree'))
    self.testee.clean()
    self.assertEmptyBackend()

  @asynctest
  async def testAsyncCleanTagged(self):
    self.assertEqual(0, self.fixture.calls)
    self.assertEmptyBackend()

    self.assertEqual('ateb+ahpla', await self.fixture.asimple('alpha', 'beta'))
    self.assertEqual('aldamg',     await self.fixture.atagged('gamma', 'delta'))
    self.assertEqual(2,            self.fixture.calls)
    self.assertEqual(4,            self.getSize())

    simpleKey = 'cache:entry:hermes.test:Fixture:asimple:' + self._arghash('alpha', 'beta')
    self.assertEqual(
      'ateb+ahpla', self.testee.mangler.loads(self.testee.backend.client.get(simpleKey))
    )

    rockTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:rock'))
    treeTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:tree'))
    self.assertFalse(rockTag == treeTag)
    self.assertEqual(22, len(rockTag))
    self.assertEqual(22, len(treeTag))

    argHash   = self._arghash('gamma', 'delta')
    tagHash   = self.testee.mangler.hashTags(dict(tree = treeTag, rock = rockTag))
    taggedKey = 'cache:entry:hermes.test:Fixture:atagged:{0}:{1}'.format(argHash, tagHash)
    self.assertEqual(
      'aldamg', self.testee.mangler.loads(self.testee.backend.client.get(taggedKey))
    )


    self.testee.clean(('rock',))
    self.assertEqual(3, self.getSize())

    self.assertEqual(
      'ateb+ahpla', self.testee.mangler.loads(self.testee.backend.client.get(simpleKey))
    )

    self.assertIsNone(self.testee.backend.client.get('cache:tag:rock'))
    self.assertEqual(
      treeTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:tree'))
    )

    # stale still accessible, though only directly
    self.assertEqual(
      'aldamg', self.testee.mangler.loads(self.testee.backend.client.get(taggedKey))
    )


    self.assertEqual('ateb+ahpla', await self.fixture.asimple('alpha', 'beta'))
    self.assertEqual('aldamg',     await self.fixture.atagged('gamma', 'delta'))
    self.assertEqual(3,            self.fixture.calls)
    self.assertEqual(5,            self.getSize(), '+1 old tagged entry')

    self.assertEqual(
      'ateb+ahpla', self.testee.mangler.loads(self.testee.backend.client.get(simpleKey))
    )

    self.assertNotEqual(
      rockTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:rock'))
    )
    rockTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:rock'))
    self.assertFalse(rockTag == treeTag)
    self.assertEqual(22, len(rockTag))
    self.assertEqual(
      treeTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:tree'))
    )

    # stale still accessible, though only directly
    self.assertEqual(
      'aldamg', self.testee.mangler.loads(self.testee.backend.client.get(taggedKey))
    )

    argHash   = self._arghash('gamma', 'delta')
    tagHash   = self.testee.mangler.hashTags(dict(tree = treeTag, rock = rockTag))
    taggedKey = 'cache:entry:hermes.test:Fixture:atagged:{0}:{1}'.format(argHash, tagHash)
    self.assertEqual(
      'aldamg', self.testee.mangler.loads(self.testee.backend.client.get(taggedKey))
    )


    self.testee.clean(('rock', 'tree'))
    self.assertEqual(3, self.getSize(), 'simaple, new tagged and old tagged')

    self.assertEqual(
      'ateb+ahpla', self.testee.mangler.loads(self.testee.backend.client.get(simpleKey))
    )

    # new stale is accessible, though only directly
    self.assertEqual(
      'aldamg', self.testee.mangler.loads(self.testee.backend.client.get(taggedKey))
    )


    self.assertEqual('ateb+ahpla', await self.fixture.asimple('alpha', 'beta'))
    self.assertEqual('aldamg',     await self.fixture.atagged('gamma', 'delta'))
    self.assertEqual(4,            self.fixture.calls)
    self.assertEqual(6,            self.getSize(), '+2 old tagged entries')

    self.assertEqual(
      'ateb+ahpla', self.testee.mangler.loads(self.testee.backend.client.get(simpleKey))
    )

    # new stale still accessible, though only directly
    self.assertEqual(
      'aldamg', self.testee.mangler.loads(self.testee.backend.client.get(taggedKey))
    )

    self.assertNotEqual(
      rockTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:rock'))
    )
    self.assertNotEqual(
      treeTag, self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:tree'))
    )

    rockTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:rock'))
    treeTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:tree'))
    self.assertFalse(rockTag == treeTag)
    self.assertEqual(22, len(rockTag))
    self.assertEqual(22, len(treeTag))

    argHash   = self._arghash('gamma', 'delta')
    tagHash   = self.testee.mangler.hashTags(dict(tree = treeTag, rock = rockTag))
    taggedKey = 'cache:entry:hermes.test:Fixture:atagged:{0}:{1}'.format(argHash, tagHash)
    self.assertEqual(
      'aldamg', self.testee.mangler.loads(self.testee.backend.client.get(taggedKey))
    )


    self.testee.clean(('rock', 'tree'))
    self.testee.clean()
    self.assertEmptyBackend()

  def testNested(self):
    self.assertEqual('beta+alpha', self.fixture.nested('alpha', 'beta'))
    self.assertEqual(2, self.fixture.calls)
    key = 'cache:entry:hermes.test:Fixture:nested:' + self._arghash('alpha', 'beta')
    self.assertEqual('beta+alpha', self.testee.mangler.loads(self.testee.backend.client.get(key)))
    key = 'cache:entry:hermes.test:Fixture:simple:' + self._arghash('beta', 'alpha')
    self.assertEqual('ahpla+ateb', self.testee.mangler.loads(self.testee.backend.client.get(key)))

  @asynctest
  async def testAsyncNested(self):
    self.assertEqual('beta+alpha', await self.fixture.anested('alpha', 'beta'))
    self.assertEqual(2, self.fixture.calls)
    key = 'cache:entry:hermes.test:Fixture:anested:' + self._arghash('alpha', 'beta')
    self.assertEqual('beta+alpha', self.testee.mangler.loads(self.testee.backend.client.get(key)))
    key = 'cache:entry:hermes.test:Fixture:asimple:' + self._arghash('beta', 'alpha')
    self.assertEqual('ahpla+ateb', self.testee.mangler.loads(self.testee.backend.client.get(key)))

  def testConcurrent(self):
    log = []
    key = lambda fn, *args, **kwargs: 'mk:{0}:{1}'.format(*args)

    @self.testee(tags = ('a', 'z'), key = key, ttl = 120)
    def bar(a, b):
      log.append(1)
      time.sleep(0.04)
      return '{0}-{1}'.format(a, b)[::2]

    threads = [threading.Thread(target = bar, args = ('alpha', 'beta')) for _ in range(4)]
    tuple(map(threading.Thread.start, threads))
    tuple(map(threading.Thread.join,  threads))

    self.assertEqual(1, sum(log))
    self.assertEqual(3, self.getSize())

    aTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:a'))
    zTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:z'))
    self.assertFalse(aTag == zTag)
    self.assertEqual(22, len(aTag))
    self.assertEqual(22, len(zTag))

    tagHash = self.testee.mangler.hashTags(dict(a = aTag, z = zTag))
    key     = 'mk:alpha:beta:' + tagHash
    self.assertEqual('apabt', self.testee.mangler.loads(self.testee.backend.client.get(key)))

    del log[:]
    self.testee.clean()
    self.testee.backend.lock = lambda k: backend.AbstractLock(k)  # now see a dogpile

    threads = [threading.Thread(target = bar, args = ('alpha', 'beta')) for _ in range(4)]
    tuple(map(threading.Thread.start, threads))
    tuple(map(threading.Thread.join,  threads))

    self.assertGreater(sum(log), 1, 'dogpile')
    # enries may be duplicated if tags overwrite
    self.assertGreaterEqual(self.getSize(), 3)

  @asynctest
  async def testAsyncConcurrent(self):
    log = []
    key = lambda fn, *args, **kwargs: 'mk:{0}:{1}'.format(*args)

    @self.testee(tags = ('a', 'z'), key = key, ttl = 120)
    async def bar(a, b):
      log.append(1)
      await asyncio.sleep(0.04)
      return '{0}-{1}'.format(a, b)[::2]

    await asyncio.gather(*(bar('alpha', 'beta') for _ in range(4)))

    self.assertEqual(1, sum(log))
    self.assertEqual(3, self.getSize())

    aTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:a'))
    zTag = self.testee.mangler.loads(self.testee.backend.client.get('cache:tag:z'))
    self.assertFalse(aTag == zTag)
    self.assertEqual(22, len(aTag))
    self.assertEqual(22, len(zTag))

    tagHash = self.testee.mangler.hashTags(dict(a = aTag, z = zTag))
    key     = 'mk:alpha:beta:' + tagHash
    self.assertEqual('apabt', self.testee.mangler.loads(self.testee.backend.client.get(key)))

    del log[:]
    self.testee.clean()
    self.testee.backend.lock = lambda k: backend.AbstractLock(k)  # now see a dogpile

    await asyncio.gather(*(bar('alpha', 'beta') for _ in range(4)))

    self.assertGreater(sum(log), 1, 'dogpile')
    # enries may be duplicated if tags overwrite
    self.assertGreaterEqual(self.getSize(), 3)


class BaseRemoteBackendLockTest(TestCase):

  ttlDelta = 0

  cache: Hermes
  testee: backend.AbstractLock

  def setUp(self):
    '''``cache` and ```testee`` are expected to be created in override.'''

    self.cache.clean()

  def getKeyTtl(self, key: str) -> int:
    raise NotImplementedError

  def testAcquire(self):
    for _ in range(2):
      try:
        self.assertTrue(self.testee.acquire(True))
        self.assertFalse(self.testee.acquire(False))
        self.assertEqual('123', self.testee.key)
        self.assertAlmostEqual(900, self.getKeyTtl(self.testee.key), delta = self.ttlDelta)
      finally:
        self.testee.release()

  def testRelease(self):
    for _ in range(2):
      try:
        self.assertTrue(self.testee.acquire(True))
        self.assertFalse(self.testee.acquire(False))
        self.assertEqual('123', self.testee.key)
      finally:
        self.testee.release()
      self.assertIs(None, self.testee.client.get(self.testee.key))

  def testWith(self):
    with self.testee:
      self.assertFalse(self.testee.acquire(False))
      self.assertEqual('123', self.testee.key)

      another = type(self.testee)('234', self.cache.backend.client)
      with another:
        self.assertFalse(another.acquire(False))
        self.assertFalse(self.testee.acquire(False))
        self.assertEqual('234', another.key)

  def testConcurrent(self):
    log = []
    check = threading.Lock()

    def target():
      with self.testee:
        log.append(check.acquire(False))
        time.sleep(0.05)
        check.release()
        time.sleep(0.05)

    threads = tuple(map(lambda _: threading.Thread(target = target), range(4)))
    tuple(map(threading.Thread.start, threads))
    tuple(map(threading.Thread.join,  threads))

    self.assertEqual([True] * 4, log)

  @asynctest
  async def testAsyncConcurrent(self):
    log = []
    check = threading.Lock()

    loop = asyncio.get_event_loop()

    async def target():
      await loop.run_in_executor(None, self.testee.acquire)
      try:
        log.append(check.acquire(False))
        await asyncio.sleep(0.05)
        check.release()
        await asyncio.sleep(0.05)
      finally:
        await loop.run_in_executor(None, self.testee.release)

    await asyncio.gather(*(target() for _ in range(4)))

    self.assertEqual([True] * 4, log)
