import builtins
import inspect
import json
import lzma
import os
import threading
import time
import types
import unittest
import zlib
from unittest import mock

from .. import Cached, CachedCoro, Compressor, Hermes, HermesError, Mangler, Serialiser, test
from ..backend import AbstractBackend, AbstractLock, inprocess
from . import asynctest


@mock.patch.object(builtins, 'print', mock.MagicMock())
class TestManualSnippets(unittest.TestCase):

  def testQuickstart(self):
    import hermes.backend.redis


    cache = hermes.Hermes(
      hermes.backend.redis.Backend,
      host = os.getenv('TEST_REDIS_HOST', 'localhost'),
      ttl = 600,
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
        return (a + b) / 2.0

    print(foo(2, 333))

    example = Example()
    print(example.bar(2, 10))
    print(example.baz(2, 10))

    foo.invalidate(2, 333)
    example.bar.invalidate(2, 10)
    example.baz.invalidate(2, 10)

    cache.clean(['math'])  # invalidate entries tagged 'math'
    cache.clean()          # flush cache

  def testNonTagged(self):
    import hermes.backend.inprocess  # noqa


    cache = hermes.Hermes(hermes.backend.inprocess.Backend)

    @cache
    def foo(a, b):
      return a * b

    foo(2, 2)
    foo(2, 4)

    print(cache.backend.dump())
    #  {
    #    'cache:entry:foo:bNapzUm_P8fjh8lhIWYgkg': 8,
    #    'cache:entry:foo:JjwE0zQhMRt_5lfwNNPk1Q': 4
    #  }

  def testTagged(self):
    import hermes.backend.inprocess  # noqa


    cache = hermes.Hermes(hermes.backend.inprocess.Backend)

    @cache(tags = ('tag1', 'tag2'))
    def foo(a, b):
      return a * b

    foo(2, 2)

    print(cache.backend.dump())
    #  {
    #    'cache:tag:tag1': 'SeL9JQMnT-_4jRN1nxeoeg',
    #    'cache:tag:tag2': 'n_OXAKlSjiz5zK5iAEe7zA',
    #    'cache:entry:foo:JjwE0zQhMRt_5lfwNNPk1Q:h_C-2mB3kWNNrA4r7byxNA': 4
    #  }

  def testTradeoff(self):
    import hermes.backend.inprocess  # noqa


    cache = hermes.Hermes(hermes.backend.inprocess.Backend)

    @cache(tags = ('tag1', 'tag2'))
    def foo(a, b):
      return a * b

    foo(2, 2)

    print(cache.backend.dump())
    #  {
    #    'cache:tag:tag1': 'Z_t4-2QfjwvYUc_d75WJgw',
    #    'cache:tag:tag2': 'M_2pg1-dfS_8OM1Dnd4mXw',
    #    'cache:entry:foo:JjwE0zQhMRt_5lfwNNPk1Q:ZuT3KKj6gttXtU01-JSbwQ': 4
    #  }

    cache.clean(['tag1'])
    foo(2, 2)

    print(cache.backend.dump())
    #  {
    #    'cache:tag:tag1': 'TAuY_hhl0a22Nm7P_dWQRA',
    #    'cache:tag:tag2': 'M_2pg1-dfS_8OM1Dnd4mXw',
    #    'cache:entry:foo:JjwE0zQhMRt_5lfwNNPk1Q:St3ZHOzerXZxN0qkzXcLVw': 4,
    #    'cache:entry:foo:JjwE0zQhMRt_5lfwNNPk1Q:ZuT3KKj6gttXtU01-JSbwQ': 4
    #  }


class TestFacade(unittest.TestCase):

  def testBackendInstanceInstantiation(self):
    mangler = Mangler()
    backend = AbstractBackend(mangler)
    testee = Hermes(backend, mangler = mangler)

    @testee
    def mul(a, b):
      return a * b

    self.assertTrue(4, mul(2, 2))

  def testBackendInstanceWarning(self):
    mangler = Mangler()
    backend = AbstractBackend(mangler)

    with self.assertWarns(Warning) as ctx:
      testee = Hermes(backend, mangler = mangler, someBackendOpt = 13)
    self.assertEqual(
      'Backend options ignored because backend instance is passed', str(ctx.warning)
    )

    @testee
    def mul(a, b):
      return a * b

    self.assertTrue(4, mul(2, 2))

  def testInvalidInstantiation(self):
    with self.assertRaises(HermesError) as ctx:
      Hermes(object())
    self.assertEqual('Expected class or instance of AbstractBackend', str(ctx.exception))


class TestDefaultMangler(unittest.TestCase):

  testee: Mangler

  def setUp(self):
    self.testee = Mangler()

  def testHash(self):
    self.assertEqual('rL0Y20zC-Fzt72VPzMSk2A', self.testee.hash(b'foo'))

  def testSerialisation(self):
    value = {'meaning': '42' * 100}
    self.assertEqual(value, self.testee.loads(self.testee.dumps(value)))

  def testSerialisationCustom(self):
    self.testee.serialiser = Serialiser(lambda obj: json.dumps(obj).encode(), json.loads)

    value = {'meaning': '42' * 100}
    self.assertEqual(value, self.testee.loads(self.testee.dumps(value)))

  def testSerialisationCompressorOptOut(self):
    self.testee.compressor = None

    value = {'meaning': '42' * 100}
    self.assertEqual(value, self.testee.loads(self.testee.dumps(value)))

  def testSerialisationCompressorCustom(self):
    self.testee.compressor = Compressor(lzma.compress, lzma.decompress, lzma.LZMAError, 100)

    value = {'meaning': '42' * 100}
    self.assertEqual(value, self.testee.loads(self.testee.dumps(value)))

  def testNameEntryFunction(self):
    def fn(*args, **kwargs):
      pass

    no_arg_hash = self.testee.hash(self.testee.dumps(((), ())))
    pos_arg_hash = self.testee.hash(self.testee.dumps((('p',), ())))
    kw_arg_hash = self.testee.hash(self.testee.dumps(((), (('a', 1), ('k', 'v')))))
    both_arg_hash = self.testee.hash(self.testee.dumps((('p',), (('k', 'v'),))))

    prefix = 'cache:entry:hermes.test.facade'
    self.assertEqual(f'{prefix}:fn:{no_arg_hash}', self.testee.nameEntry(fn))
    self.assertEqual(f'{prefix}:fn:{pos_arg_hash}', self.testee.nameEntry(fn, 'p'))
    self.assertEqual(f'{prefix}:fn:{kw_arg_hash}', self.testee.nameEntry(fn, k = 'v', a = 1))
    self.assertEqual(f'{prefix}:fn:{both_arg_hash}', self.testee.nameEntry(fn, 'p', k = 'v'))

  def testNameEntryMethod(self):
    class Cls:

      def meth(self):
        pass

      @classmethod
      def clsmeth(cls):
        pass

      @staticmethod
      def statmeth():
        pass

    obj = Cls()
    prefix = 'cache:entry:hermes.test.facade'

    testfn = self.testee.nameEntry
    no_arg_hash = self.testee.hash(self.testee.dumps(((), ())))
    pos_arg_hash = self.testee.hash(self.testee.dumps((('p',), ())))
    kw_arg_hash = self.testee.hash(self.testee.dumps(((), (('a', 1), ('k', 'v')))))
    both_arg_hash = self.testee.hash(self.testee.dumps((('p',), (('k', 'v'),))))

    self.assertEqual(f'{prefix}:meth:{no_arg_hash}', testfn(Cls.meth))
    self.assertEqual(f'{prefix}:meth:{pos_arg_hash}', testfn(Cls.meth, 'p'))
    self.assertEqual(f'{prefix}:meth:{kw_arg_hash}', testfn(Cls.meth, k = 'v', a = 1))
    self.assertEqual(f'{prefix}:meth:{both_arg_hash}', testfn(Cls.meth, 'p', k = 'v'))

    self.assertEqual(f'{prefix}:type:clsmeth:{no_arg_hash}', testfn(Cls.clsmeth))
    self.assertEqual(f'{prefix}:type:clsmeth:{pos_arg_hash}', testfn(Cls.clsmeth, 'p'))
    self.assertEqual(f'{prefix}:type:clsmeth:{kw_arg_hash}', testfn(Cls.clsmeth, k = 'v', a = 1))
    self.assertEqual(f'{prefix}:type:clsmeth:{both_arg_hash}', testfn(Cls.clsmeth, 'p', k = 'v'))

    self.assertEqual(f'{prefix}:statmeth:{no_arg_hash}', testfn(Cls.statmeth))
    self.assertEqual(f'{prefix}:statmeth:{pos_arg_hash}', testfn(Cls.statmeth, 'p'))
    self.assertEqual(f'{prefix}:statmeth:{kw_arg_hash}', testfn(Cls.statmeth, k = 'v', a = 1))
    self.assertEqual(f'{prefix}:statmeth:{both_arg_hash}', testfn(Cls.statmeth, 'p', k = 'v'))

    self.assertEqual(f'{prefix}:Cls:meth:{no_arg_hash}', testfn(obj.meth))
    self.assertEqual(f'{prefix}:Cls:meth:{pos_arg_hash}', testfn(obj.meth, 'p'))
    self.assertEqual(f'{prefix}:Cls:meth:{kw_arg_hash}', testfn(obj.meth, k = 'v', a = 1))
    self.assertEqual(f'{prefix}:Cls:meth:{both_arg_hash}', testfn(obj.meth, 'p', k = 'v'))

    self.assertEqual(f'{prefix}:type:clsmeth:{no_arg_hash}', testfn(obj.clsmeth))
    self.assertEqual(f'{prefix}:type:clsmeth:{pos_arg_hash}', testfn(obj.clsmeth, 'p'))
    self.assertEqual(f'{prefix}:type:clsmeth:{kw_arg_hash}', testfn(obj.clsmeth, k = 'v', a = 1))
    self.assertEqual(f'{prefix}:type:clsmeth:{both_arg_hash}', testfn(obj.clsmeth, 'p', k = 'v'))

    self.assertEqual(f'{prefix}:statmeth:{no_arg_hash}', testfn(obj.statmeth))
    self.assertEqual(f'{prefix}:statmeth:{pos_arg_hash}', testfn(obj.statmeth, 'p'))
    self.assertEqual(f'{prefix}:statmeth:{kw_arg_hash}', testfn(obj.statmeth, k = 'v', a = 1))
    self.assertEqual(f'{prefix}:statmeth:{both_arg_hash}', testfn(obj.statmeth, 'p', k = 'v'))

  def testNameEntryCallableObject(self):
    class UnnamedCallable:

      def __call__(self, *args, **kwargs):
        pass

    prefix = 'cache:entry:hermes.test.facade'

    obj = UnnamedCallable()

    with self.assertRaises(HermesError) as ctx:
      self.testee.nameEntry(obj)
    self.assertEqual(
      'fn is callable but its name is undefined, consider overriding Mangler.nameEntry',
      str(ctx.exception),
    )

    class NamedCallable(UnnamedCallable):

      @property
      def __name__(self):
        return 'd.b'

    no_arg_hash = self.testee.hash(self.testee.dumps(((), ())))
    pos_arg_hash = self.testee.hash(self.testee.dumps((('p',), ())))
    kw_arg_hash = self.testee.hash(self.testee.dumps(((), (('a', 1), ('k', 'v')))))
    both_arg_hash = self.testee.hash(self.testee.dumps((('p',), (('k', 'v'),))))

    obj = NamedCallable()
    self.assertEqual(f'{prefix}:d.b:{no_arg_hash}', self.testee.nameEntry(obj))
    self.assertEqual(f'{prefix}:d.b:{pos_arg_hash}', self.testee.nameEntry(obj, 'p'))
    self.assertEqual(f'{prefix}:d.b:{kw_arg_hash}', self.testee.nameEntry(obj, k = 'v', a = 1))
    self.assertEqual(f'{prefix}:d.b:{both_arg_hash}', self.testee.nameEntry(obj, 'p', k = 'v'))

  def testNameEntryUncallable(self):
    with self.assertRaises(HermesError) as ctx:
      self.testee.nameEntry({'foo': 'bar'})
    self.assertEqual('fn is expected to be callable', str(ctx.exception))

  def testNameTag(self):
    self.assertEqual('cache:tag:foo', self.testee.nameTag('foo'))

  def testMapTags(self):
    self.assertEqual({}, self.testee.mapTags([]))

    actual = self.testee.mapTags(['foo', 'bar'])
    self.assertEqual(2, len(actual))
    self.assertIn('foo', actual)
    self.assertIn('bar', actual)
    self.assertNotEqual(actual, self.testee.mapTags({'foo'}))

  def testHashTags(self):
    # Normally a combination of nameTag() and mapTags()
    tagMap = {'cache:tag:a': '2209aaab3ace901e', 'cache:tag:z': '92670722746eda09'}
    self.assertEqual('Iq0ue2khRbyyTyLZJecJEA', self.testee.hashTags(tagMap))

  def testNameLock(self):
    self.assertEqual('cache:lock:foo.bar', self.testee.nameLock('foo.bar'))
    self.assertEqual(
      'cache:lock:hermes.test:Fixture:tagged:78d64ea049a57494',
      self.testee.nameLock('cache:entry:hermes.test:Fixture:tagged:78d64ea049a57494'),
    )


class TestCachedWrapping(test.TestCase):

  def setUp(self):
    mangler = Mangler()
    backend = inprocess.Backend(mangler, ttlWatchSleep = 0.001)
    self.testee = Hermes(backend, mangler = mangler)
    self.addCleanup(self.testee.backend.stopWatch)
    self.fixture = test.createFixture(self.testee)

  def testFunction(self):

    @self.testee
    def foo(a, b):
      '''Overwhelmed as one would be...'''

      return a * b

    self.assertTrue(isinstance(foo, Cached))
    self.assertEqual('foo', foo.__name__)
    self.assertEqual('Overwhelmed as one would be...', foo.__doc__)

  def testMethod(self):
    self.assertTrue(isinstance(self.fixture.simple, Cached))
    self.assertEqual('simple', self.fixture.simple.__name__)
    self.assertEqual(
      'Here be dragons... seriously just a docstring test.', self.fixture.simple.__doc__)

  def testInstanceIsolation(self):
    testee = Hermes()

    class Fixture:

      def __init__(self, marker):
        self.marker = marker

      @testee
      def foo(self):
        return self.marker

      def bar(self):
        pass

    f1 = Fixture(12)
    f2 = Fixture(24)

    # verify Cached instances are not shared
    self.assertIsNot(f1.foo, f2.foo)
    self.assertIsNot(f1.foo, f1.foo)
    # like it is normally the case of MethodType instances
    self.assertIsNot(f1.bar, f2.bar)
    self.assertIsNot(f1.bar, f1.bar)

    self.assertEqual(12, f1.foo())
    self.assertEqual(24, f2.foo())

  def testMethodDescriptor(self):

    class Fixture:

      @self.testee
      @classmethod
      def classmethod(cls):
        return cls.__name__

      @self.testee
      @staticmethod
      def staticmethod():
        return 'static'

    self.assertEqual('Fixture', Fixture().classmethod())
    self.assertEqual('static', Fixture().staticmethod())

  @asynctest
  async def testCoroutineFunction(self):
    testee = Hermes(inprocess.AsyncBackend)

    @testee
    async def foo(a, b):
      '''Placed in my position...'''

      return a * b

    self.assertTrue(isinstance(foo, CachedCoro))
    self.assertEqual('foo', foo.__name__)
    self.assertEqual('Placed in my position...', foo.__doc__)
    self.assertEqual(4, await foo(2, 2))

  @asynctest
  async def testMethodDescriptorCoroutineFunction(self):
    testee = Hermes(inprocess.AsyncBackend)

    class Fixture:

      @testee
      @classmethod
      def sclassmethod(cls):
        return cls.__name__

      @testee
      @staticmethod
      def sstaticmethod():
        return 'static'

      @testee
      @classmethod
      async def aclassmethod(cls):
        return cls.__name__[::-1]

      @testee
      @staticmethod
      async def astaticmethod():
        return 'citats'

    fixture = Fixture()
    self.assertEqual('Fixture', fixture.sclassmethod())
    self.assertEqual('static', fixture.sstaticmethod())
    self.assertEqual('erutxiF', await fixture.aclassmethod())
    self.assertEqual('citats', await fixture.astaticmethod())

    self.assertIsInstance(fixture.sclassmethod, Cached)
    self.assertIsInstance(fixture.sstaticmethod, Cached)
    self.assertIsInstance(fixture.aclassmethod, CachedCoro)
    self.assertIsInstance(fixture.astaticmethod, CachedCoro)

  def testDoubleCache(self):

    class Fixture:

      @self.testee
      @self.testee
      def doublecache(self):
        return 'descriptor vs callable'

    self.assertEqual('descriptor vs callable', Fixture().doublecache())

  def testNumbaCpuDispatcher(self):
    # In case of application of ``jit`` to a method, ``CpuDispatcher`` is
    # a descriptor which returns normal MethodType. In case of function,
    # ``CpuDispatcher`` is a callable and has ``__name__`` of the wrapped function.

    class CpuDispatcher:

      def __init__(self, fn):
        self.fn = fn

      @property
      def __name__(self):
        return self.fn.__name__

      def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)

    def jit(fn):
      return CpuDispatcher(fn)

    @self.testee
    @jit
    def sum(x, y):
      return x + y

    @self.testee
    @jit
    def product(x, y):
      return x * y

    self.assertEqual(36, sum(26, 10))
    self.assertEqual(260, product(26, 10))

  def testNamelessObjectWrapperFailure(self):

    class CpuDispatcher:

      def __init__(self, fn):
        self.fn = fn

      def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)

    def objwrap(fn):
      return CpuDispatcher(fn)

    @self.testee
    @objwrap
    def f(x, y):
      return x + y

    with self.assertRaises(HermesError) as ctx:
      f(26, 10)
    self.assertEqual(
      'fn is callable but its name is undefined, consider overriding Mangler.nameEntry',
      str(ctx.exception))

  def testUncallable(self):
    with self.assertRaises(HermesError) as ctx:
      self.testee({'meaning': 42})
    self.assertEqual(
      'First positional argument must be coroutine function, callable or method descriptor',
      str(ctx.exception),
    )

  def testClassAccess(self):
    self.assertIsInstance(self.fixture.__class__.simple, Cached)
    self.assertIsInstance(self.fixture.__class__.simple._callable, types.FunctionType)

    self.assertIsInstance(self.fixture.simple, Cached)
    self.assertIsInstance(self.fixture.simple._callable, types.MethodType)

  def testInvalidate(self):
    for _ in range(4):
      self.assertEqual('ateb+ahpla', self.fixture.simple('alpha', 'beta'))

    self.fixture.simple.invalidate('beta', 'gamma')
    self.assertNotEqual({}, self.testee.backend.dump())

    self.fixture.simple.invalidate('alpha', 'beta')
    self.assertEqual({}, self.testee.backend.dump())

  def testInvalidateFailPartialTags(self):
    for _ in range(4):
      self.assertEqual('ae-hl', self.fixture.tagged('alpha', 'beta'))

    # Simulate missing tag entry
    self.testee.backend.remove('cache:tag:tree')

    # Invalidation call does not have effect
    self.fixture.tagged.invalidate('alpha', 'beta')

    self.assertNotEqual({}, self.testee.backend.dump())
    self.assertEqual(2, len(self.testee.backend.dump()))

    # Recover missing tag
    for _ in range(4):
      self.assertEqual('ae-hl', self.fixture.tagged('alpha', 'beta'))

    self.fixture.tagged.invalidate('alpha', 'beta')
    self.assertNotEqual({}, self.testee.backend.dump())


class CustomMangler(Mangler):

  prefix = 'hermes'

  compressor = Compressor(zlib.compress, zlib.decompress, zlib.error, 0)

  def hash(self, value):
    return str(hash(value))


class TestDictCustomMangler(test.TestCase):

  def setUp(self):
    self.testee = Hermes(
      inprocess.Backend, mangler = CustomMangler(), ttl = 360, ttlWatchSleep = 0.01
    )
    self.addCleanup(self.testee.backend.stopWatch)

    self.fixture = test.createFixture(self.testee)

    self.testee.clean()

  def testSimple(self):
    self.assertEqual(0,  self.fixture.calls)
    self.assertEqual({}, self.testee.backend.dump())

    for _ in range(4):
      self.assertEqual('ateb+ahpla', self.fixture.simple('alpha', 'beta'))
      self.assertEqual(1, self.fixture.calls)
      key = 'hermes:entry:hermes.test:Fixture:simple:' + str(self._arghash('alpha', 'beta'))
      self.assertEqual({key: 'ateb+ahpla'}, self.testee.backend.dump())

    self.fixture.simple.invalidate('alpha', 'beta')
    self.assertEqual({}, self.testee.backend.dump())


    self.assertEqual(1,  self.fixture.calls)
    self.assertEqual({}, self.testee.backend.dump())

    expected = "]}'atled' :'ammag'{[+}]'ateb'[ :'ahpla'{"
    for _ in range(4):
      self.assertEqual(expected, self.fixture.simple({'alpha': ['beta']}, [{'gamma': 'delta'}]))
      self.assertEqual(2, self.fixture.calls)
      argHash = str(self._arghash({'alpha': ['beta']}, [{'gamma': 'delta'}]))
      self.assertEqual(
        {'hermes:entry:hermes.test:Fixture:simple:' + argHash: expected},
        self.testee.backend.dump())

    self.fixture.simple.invalidate({'alpha': ['beta']}, [{'gamma': 'delta'}])
    self.assertEqual({}, self.testee.backend.dump())

  def testTagged(self):
    self.assertEqual(0,  self.fixture.calls)
    self.assertEqual({}, self.testee.backend.dump())

    for _ in range(4):
      self.assertEqual('ae-hl', self.fixture.tagged('alpha', 'beta'))
      self.assertEqual(1,       self.fixture.calls)

      cache = self.testee.backend.dump()
      self.assertTrue(3, len(cache))
      self.assertFalse(cache.get('hermes:tag:tree') == cache.get('hermes:tag:rock'))
      self.assertTrue(int(cache.pop('hermes:tag:rock')) != 0)
      self.assertTrue(int(cache.pop('hermes:tag:tree')) != 0)

      expected = 'hermes:entry:hermes.test:Fixture:tagged:' + str(self._arghash('alpha', 'beta'))
      self.assertEqual(expected, ':'.join(tuple(cache.keys())[0].split(':')[:-1]))
      self.assertEqual('ae-hl', tuple(cache.values())[0])

    self.fixture.tagged.invalidate('alpha', 'beta')

    cache = self.testee.backend.dump()
    self.assertEqual(2, len(cache))
    rockTag = cache.get('hermes:tag:rock')
    treeTag = cache.get('hermes:tag:tree')
    self.assertNotEqual(rockTag, treeTag)
    self.assertTrue(int(rockTag) != 0)
    self.assertTrue(int(treeTag) != 0)

    for _ in range(4):
      self.assertEqual('ae-hl', self.fixture.tagged('alpha', 'beta'))
      self.assertEqual('ae%hl', self.fixture.tagged2('alpha', 'beta'))
      self.assertEqual(3, self.fixture.calls)

      cache = self.testee.backend.dump()
      self.assertEqual(5,  len(cache))
      self.assertEqual(rockTag, cache.get('hermes:tag:rock'))
      self.assertEqual(treeTag, cache.get('hermes:tag:tree'))
      self.assertTrue(int(cache.get('hermes:tag:ice')) != 0)

    self.testee.clean(['rock'])

    cache = self.testee.backend.dump()
    self.assertEqual(4, len(cache))
    self.assertTrue('hermes:tag:rock' not in cache)
    iceTag = cache.get('hermes:tag:ice')

    for _ in range(4):
      self.assertEqual('ae-hl', self.fixture.tagged('alpha', 'beta'))
      self.assertEqual('ae%hl', self.fixture.tagged2('alpha', 'beta'))
      self.assertEqual(5, self.fixture.calls)

      cache = self.testee.backend.dump()
      self.assertEqual(7,  len(cache), 'has new and old entries for tagged and tagged 2 + 3 tags')
      self.assertEqual(treeTag, cache.get('hermes:tag:tree'))
      self.assertEqual(iceTag,  cache.get('hermes:tag:ice'))
      self.assertTrue(int(cache.get('hermes:tag:rock')) != 0)
      self.assertNotEqual(rockTag, cache.get('hermes:tag:rock'))

  def testFunction(self):
    counter = dict(foo = 0, bar = 0)

    @self.testee
    def foo(a, b):
      counter['foo'] += 1
      return '{0}+{1}'.format(a, b)[::-1]

    key = lambda _fn, *args, **kwargs: 'mk:{0}:{1}'.format(*args)

    @self.testee(tags = ('a', 'z'), key = key, ttl = 120)
    def bar(a, b):
      counter['bar'] += 1
      return '{0}-{1}'.format(a, b)[::2]


    self.assertEqual(0,  counter['foo'])
    self.assertEqual({}, self.testee.backend.dump())

    for _ in range(4):
      self.assertEqual('ateb+ahpla', foo('alpha', 'beta'))
      self.assertEqual(1, counter['foo'])
      argHash = self._arghash('alpha', 'beta')
      self.assertEqual(
        {'hermes:entry:hermes.test.facade:foo:' + str(argHash): 'ateb+ahpla'},
        self.testee.backend.dump()
      )

    foo.invalidate('alpha', 'beta')
    self.assertEqual(1,  counter['foo'])
    self.assertEqual({}, self.testee.backend.dump())


    self.assertEqual(0,  counter['bar'])
    self.assertEqual({}, self.testee.backend.dump())

    for _ in range(4):
      self.assertEqual('apabt', bar('alpha', 'beta'))
      self.assertEqual(1,       counter['bar'])

      cache = self.testee.backend.dump()
      self.assertTrue(cache.get('hermes:tag:a') != cache.get('hermes:tag:z'))
      self.assertTrue(int(cache.pop('hermes:tag:a')) != 0)
      self.assertTrue(int(cache.pop('hermes:tag:z')) != 0)

      self.assertEqual('mk:alpha:beta', ':'.join(tuple(cache.keys())[0].split(':')[:-1]))
      self.assertEqual('apabt', tuple(cache.values())[0])

    bar.invalidate('alpha', 'beta')


    self.assertEqual(1,  counter['foo'])

    cache = self.testee.backend.dump()
    self.assertTrue(cache.get('hermes:tag:a') != cache.get('hermes:tag:z'))
    self.assertTrue(int(cache.pop('hermes:tag:a')) != 0)
    self.assertTrue(int(cache.pop('hermes:tag:z')) != 0)

  def testKey(self):
    self.assertEqual(0,  self.fixture.calls)
    self.assertEqual({}, self.testee.backend.dump())

    for _ in range(4):
      self.assertEqual('apabt', self.fixture.key('alpha', 'beta'))
      self.assertEqual(1,       self.fixture.calls)

      cache = self.testee.backend.dump()
      self.assertTrue(cache.get('hermes:tag:ash') != cache.get('hermes:tag:stone'))
      self.assertTrue(int(cache.pop('hermes:tag:ash')) != 0)
      self.assertTrue(int(cache.pop('hermes:tag:stone')) != 0)

      self.assertEqual('mykey:alpha:beta', ':'.join(tuple(cache.keys())[0].split(':')[:-1]))
      self.assertEqual('apabt', tuple(cache.values())[0])

    self.fixture.key.invalidate('alpha', 'beta')

    cache = self.testee.backend.dump()
    self.assertTrue(cache.get('hermes:tag:ash') != cache.get('hermes:tag:stone'))
    self.assertTrue(int(cache.pop('hermes:tag:ash')) != 0)
    self.assertTrue(int(cache.pop('hermes:tag:stone')) != 0)

  def testAll(self):
    self.assertEqual(0,  self.fixture.calls)
    self.assertEqual({}, self.testee.backend.dump())

    for _ in range(4):
      self.assertEqual({'a': 1, 'b': {'b': 'beta'}}, self.fixture.all({'alpha': 1}, ['beta']))
      self.assertEqual(1, self.fixture.calls)

      cache = self.testee.backend.dump()
      self.assertEqual(3, len(cache))
      self.assertTrue(int(cache.pop('hermes:tag:a')) != 0)
      self.assertTrue(int(cache.pop('hermes:tag:z')) != 0)

      expected = "mk:{'alpha':1}:['beta']"
      self.assertEqual(expected, ':'.join(tuple(cache.keys())[0].split(':')[:-1]))
      self.assertEqual({'a': 1, 'b': {'b': 'beta'}}, tuple(cache.values())[0])

    self.fixture.all.invalidate({'alpha': 1}, ['beta'])

    cache = self.testee.backend.dump()
    self.assertEqual(2, len(cache))
    self.assertTrue(int(cache.pop('hermes:tag:a')) != 0)
    self.assertTrue(int(cache.pop('hermes:tag:z')) != 0)

  def testClean(self):
    self.assertEqual(0,  self.fixture.calls)
    self.assertEqual({}, self.testee.backend.dump())

    self.assertEqual('ateb+ahpla', self.fixture.simple('alpha', 'beta'))
    self.assertEqual('aldamg',     self.fixture.tagged('gamma', 'delta'))
    self.assertEqual(2,            self.fixture.calls)

    self.testee.clean()

    self.assertEqual(2,  self.fixture.calls)
    self.assertEqual({}, self.testee.backend.dump())

  def testCleanTagged(self):
    self.assertEqual(0,  self.fixture.calls)
    self.assertEqual({}, self.testee.backend.dump())

    self.assertEqual('ateb+ahpla', self.fixture.simple('alpha', 'beta'))
    self.assertEqual('aldamg',     self.fixture.tagged('gamma', 'delta'))
    self.assertEqual(2,            self.fixture.calls)

    cache = self.testee.backend.dump()
    self.assertTrue(4, len(cache))
    self.assertEqual(
      'ateb+ahpla',
      cache.pop(
        'hermes:entry:hermes.test:Fixture:simple:' + str(self._arghash('alpha', 'beta'))
      ),
    )
    self.assertFalse(cache.get('hermes:tag:tree') == cache.get('hermes:tag:rock'))
    self.assertTrue(int(cache.pop('hermes:tag:rock')) != 0)
    self.assertTrue(int(cache.pop('hermes:tag:tree')) != 0)

    expected = 'hermes:entry:hermes.test:Fixture:tagged:' + str(self._arghash('gamma', 'delta'))
    self.assertEqual(expected, ':'.join(tuple(cache.keys())[0].split(':')[:-1]))
    self.assertEqual('aldamg', tuple(cache.values())[0])


    self.testee.clean(('rock',))

    cache = self.testee.backend.dump()
    self.assertTrue(3, len(cache))
    self.assertEqual(
      'ateb+ahpla',
      cache.pop(
        'hermes:entry:hermes.test:Fixture:simple:' + str(self._arghash('alpha', 'beta'))
      ),
    )
    self.assertTrue(int(cache.pop('hermes:tag:tree')) != 0)
    self.assertFalse('hermes:tag:rock' in cache)

    self.assertEqual(expected, ':'.join(tuple(cache.keys())[0].split(':')[:-1]))
    self.assertEqual('aldamg', tuple(cache.values())[0])


    self.assertEqual('ateb+ahpla', self.fixture.simple('alpha', 'beta'))
    self.assertEqual('aldamg',     self.fixture.tagged('gamma', 'delta'))
    self.assertEqual(3,            self.fixture.calls)

    cache = self.testee.backend.dump()
    self.assertTrue(4, len(cache))
    self.assertEqual(
      'ateb+ahpla',
      cache.pop(
        'hermes:entry:hermes.test:Fixture:simple:' + str(self._arghash('alpha', 'beta'))
      ),
    )
    self.assertFalse(cache.get('hermes:tag:tree') == cache.get('hermes:tag:rock'))
    self.assertTrue(int(cache.pop('hermes:tag:rock')) != 0)
    self.assertTrue(int(cache.pop('hermes:tag:tree')) != 0)

    self.assertEqual(expected, ':'.join(tuple(cache.keys())[0].split(':')[:-1]))
    self.assertEqual('aldamg', tuple(cache.values())[0])


    self.testee.clean(('rock', 'tree'))

    cache = self.testee.backend.dump()
    self.assertTrue(2, len(cache))
    self.assertEqual(
      'ateb+ahpla',
      cache.pop(
        'hermes:entry:hermes.test:Fixture:simple:' + str(self._arghash('alpha', 'beta'))
      ),
    )
    self.assertFalse('hermes:tag:tree' in cache)
    self.assertFalse('hermes:tag:rock' in cache)

    self.assertEqual(expected, ':'.join(tuple(cache.keys())[0].split(':')[:-1]))
    self.assertEqual('aldamg', tuple(cache.values())[0])


    self.assertEqual('ateb+ahpla', self.fixture.simple('alpha', 'beta'))
    self.assertEqual('aldamg',     self.fixture.tagged('gamma', 'delta'))
    self.assertEqual(4,            self.fixture.calls)

    cache = self.testee.backend.dump()
    self.assertTrue(4, len(cache))
    self.assertEqual(
      'ateb+ahpla',
      cache.pop(
        'hermes:entry:hermes.test:Fixture:simple:' + str(self._arghash('alpha', 'beta'))
      ),
    )
    self.assertFalse(cache.get('hermes:tag:tree') == cache.get('hermes:tag:rock'))
    self.assertTrue(int(cache.pop('hermes:tag:rock')) != 0)
    self.assertTrue(int(cache.pop('hermes:tag:tree')) != 0)

    self.assertEqual(expected, ':'.join(tuple(cache.keys())[0].split(':')[:-1]))
    self.assertEqual('aldamg', tuple(cache.values())[0])


    self.testee.clean()

    self.assertEqual(4,  self.fixture.calls)
    self.assertEqual({}, self.testee.backend.dump())

  def testNested(self):
    self.assertEqual('beta+alpha', self.fixture.nested('alpha', 'beta'))
    self.assertEqual(2, self.fixture.calls)
    prefix = 'hermes:entry:hermes.test:Fixture'
    self.assertEqual({
      prefix + ':nested:' + str(self._arghash('alpha', 'beta')): 'beta+alpha',
      prefix + ':simple:' + str(self._arghash('beta', 'alpha')): 'ahpla+ateb'
    }, self.testee.backend.dump())

  def testConcurrent(self):
    log = []
    key = lambda _fn, *args, **kwargs: 'mk:{0}:{1}'.format(*args)

    @self.testee(tags = ('a', 'z'), key = key, ttl = 120)
    def bar(a, b):
      log.append(1)
      time.sleep(0.04)
      return '{0}-{1}'.format(a, b)[::2]

    threads = [threading.Thread(target = bar, args = ('alpha', 'beta')) for _ in range(4)]
    tuple(map(threading.Thread.start, threads))
    tuple(map(threading.Thread.join,  threads))

    self.assertEqual(1, sum(log))

    cache = self.testee.backend.dump()
    self.assertTrue(int(cache.pop('hermes:tag:a')) != 0)
    self.assertTrue(int(cache.pop('hermes:tag:z')) != 0)

    self.assertEqual('mk:alpha:beta', ':'.join(tuple(cache.keys())[0].split(':')[:-1]))
    self.assertEqual('apabt', tuple(cache.values())[0])

    del log[:]
    self.testee.clean()
    self.testee.backend.lock = lambda k: AbstractLock(k)  # now see a dogpile

    threads = [threading.Thread(target = bar, args = ('alpha', 'beta')) for _ in range(4)]
    tuple(map(threading.Thread.start, threads))
    tuple(map(threading.Thread.join,  threads))

    self.assertGreater(sum(log), 1, 'dogpile')

    cache = self.testee.backend.dump()
    self.assertTrue(int(cache.pop('hermes:tag:a')) != 0)
    self.assertTrue(int(cache.pop('hermes:tag:z')) != 0)

    self.assertEqual('mk:alpha:beta', ':'.join(tuple(cache.keys())[0].split(':')[:-1]))
    self.assertEqual('apabt', tuple(cache.values())[0])


class CustomCached(Cached):

  def __call__(self, *args, **kwargs):
    ''''Override to add bypass when backend is down.'''

    try:
      return super().__call__(*args, **kwargs)
    except RuntimeError:
      return self._callable(*args, **kwargs)


class BackendThatIsDown(inprocess.Backend):

  def load(self, keys):
    raise RuntimeError('Backend is down')


class TestDictCustomCached(test.TestCase):

  def setUp(self):
    self.testee = Hermes(
      BackendThatIsDown, cachedfactory = self.cachedfactory, ttl = 360, ttlWatchSleep = 0.01
    )
    self.fixture = test.createFixture(self.testee)

    self.testee.clean()

  def cachedfactory(self, frontend: Hermes, fn, **kwargs) -> Cached:
    if inspect.iscoroutinefunction(fn):
      return CachedCoro(frontend, fn, **kwargs)
    elif callable(fn) or inspect.ismethoddescriptor(fn):
      return CustomCached(frontend, fn, **kwargs)
    else:
      raise HermesError(
        'First positional argument must be coroutine function, callable or method descriptor'
      )

  def testSimple(self):
    self.assertEqual(0,  self.fixture.calls)
    self.assertEqual({}, self.testee.backend.dump())

    for i in range(4):
      self.assertEqual('ateb+ahpla', self.fixture.simple('alpha', 'beta'))
      self.assertEqual(i + 1, self.fixture.calls)
      self.assertEqual({}, self.testee.backend.dump())
