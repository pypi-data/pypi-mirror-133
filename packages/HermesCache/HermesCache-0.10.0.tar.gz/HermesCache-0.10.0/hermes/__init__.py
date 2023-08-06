import asyncio
import base64
import functools
import hashlib
import inspect
import os
import pickle
import types
import typing
import warnings
import zlib
from typing import Any, Callable, Coroutine, Dict, Iterable, Optional, Sequence, Tuple, Type, Union

from .backend import AbstractBackend


__all__ = 'Hermes', 'HermesError', 'Mangler', 'Cached', 'CachedCoro', 'Serialiser', 'Compressor'


class Serialiser(typing.NamedTuple):
  '''Serialisation delegate.'''

  dumps: Callable[[Any], bytes]
  '''Serialise cache value.'''

  loads: Callable[[bytes], Any]
  '''Deserialise cache value.'''


class Compressor(typing.NamedTuple):
  '''Compression delegate.'''

  compress: Callable[[bytes], bytes]
  '''Compress serialised cache value.'''

  decompress: Callable[[bytes], bytes]
  '''Decompress serialised cache value.'''

  decompressError: Union[Type[Exception], Tuple[Type[Exception], ...]]
  '''Decompression error(s) that indicate uncompressed payload.'''

  compressMinLength: int = 0
  '''Minimal length of payload in bytes to trigger compression.'''


class Mangler:
  '''Key manager responsible for creating keys, hashing and serialisation.'''

  prefix = 'cache'
  '''Prefix for cache and tag entries.'''

  serialiser = Serialiser(pickle.dumps, pickle.loads)
  '''Serialisation delegate.'''

  compressor = Compressor(zlib.compress, zlib.decompress, zlib.error, 100)
  '''Optional compression delegate.'''

  def hash(self, value: bytes) -> str:
    '''
    Hash value.

    :return: base64 encoded MD5 hash of the value.
    '''

    return base64.urlsafe_b64encode(hashlib.md5(value).digest()).strip(b'=').decode()

  def dumps(self, value) -> bytes:
    '''Serialise and conditionally compress value.'''

    result = self.serialiser.dumps(value)
    if self.compressor and len(result) >= self.compressor.compressMinLength:
      result = self.compressor.compress(result)

    return result

  def loads(self, value: bytes):
    '''Conditionally decompress and deserialise value.'''

    if self.compressor:
      try:
        value = self.compressor.decompress(value)
      except self.compressor.decompressError:
        # It is expected that the error indicates that the value is
        # shorter than compressMinLength
        pass

    return self.serialiser.loads(value)

  def nameEntry(self, fn: Callable, *args, **kwargs) -> str:
    '''
    Return cache key for given callable and its positional and
    keyword arguments.

    Note how callable, ``fn``, is represented in the cache key:

      1) a ``types.MethodType`` instance -> names of
         ``(module, class, method)``
      2) a ``types.FunctionType`` instance -> names of
         ``(module, function)``
      3) other callalbe objects with ``__name__`` -> name of
         ``(module, object)``

    This means that if two function are defined dynamically in the
    same module with same names, like::

      def createF1():
          @cache
          def f(a, b):
              return a + b
          return f

      def createF2():
          @cache
          def f(a, b):
              return a * b
          return f

      print(createF1()(1, 2))
      print(createF2()(1, 2))

    Both will return `3`, because cache keys will clash. In such cases
    you need to pass ``key`` with custom key function.

    It can also be that an object in case 3 doesn't have name, or its
    name isn't unique, then a ``nameEntry`` should be overridden with
    something that represents it uniquely, like
    ``repr(fn).rsplit(' at 0x', 1)[0]`` (address should be stripped so
    after Python process restart the cache can still be valid
    and usable).
    '''

    result = [self.prefix, 'entry']
    if callable(fn):
      try:
        # types.MethodType
        result.extend([
          fn.__module__,
          fn.__self__.__class__.__name__,  # type: ignore[attribute-error]
          fn.__name__,
        ])
      except AttributeError:
        try:
          # types.FunctionType and other object with __name__
          result.extend([fn.__module__, fn.__name__])
        except AttributeError:
          raise HermesError(
            'fn is callable but its name is undefined, consider overriding Mangler.nameEntry'
          )
    else:
      raise HermesError('fn is expected to be callable')

    arguments = args, tuple(sorted(kwargs.items()))
    result.append(self.hash(self.dumps(arguments)))

    return ':'.join(result)

  def nameTag(self, tag: str) -> str:
    '''Build fully qualified backend tag name.'''

    return ':'.join([self.prefix, 'tag', tag])

  def mapTags(self, tagKeys: Iterable[str]) -> Dict[str, str]:
    '''Map tags to random values for seeding.'''

    rnd = os.urandom(4).hex()
    return {key: self.hash(':'.join((key, rnd)).encode()) for key in tagKeys}

  def hashTags(self, tagMap: Dict[str, str]) -> str:
    '''Hash tags of a cache entry for the entry key,'''

    values = tuple(zip(*sorted(tagMap.items())))[1]  # sorted by key dict values
    return self.hash(':'.join(values).encode())

  def nameLock(self, entryKey: str) -> str:
    '''
    Create fully qualified backend lock key for the entry key.

    :param entryKey:
      Entry key to create a lock key for. If given entry key is already
      a colon-separated key name with first component equal to
      :attr:`prefix`, first to components are dropped. For instance:

      - ``foo`` → ``cache:lock:foo``
      - ``cache:entry:fn:tagged:78d64ea049a57494`` →
        ``cache:lock:fn:tagged:78d64ea049a57494``

    '''

    parts = entryKey.split(':')
    if parts[0] == self.prefix:
      entryKey = ':'.join(parts[2:])

    return ':'.join([self.prefix, 'lock', entryKey])


class Cached:
  '''Cache-point wrapper for callables and descriptors.'''

  _frontend: 'Hermes'
  '''
  Hermes instance which provides backend and mangler instances, and
  TTL fallback value.
  '''

  _callable: Callable
  '''
  The decorated callable, stays ``types.FunctionType`` if a function
  is decorated, otherwise it is transformed to ``types.MethodType``
  on the instance clone by descriptor protocol implementation. It can
  also be a method descriptor which is also transformed accordingly to
  the descriptor protocol (e.g. ``staticmethod`` and ``classmethod``).
  '''

  _isDescriptor: bool
  '''Flag defining if the callable is a method descriptor.'''

  _isMethod: bool
  '''Flag defining if the callable is a method.'''

  _ttl: Optional[int]
  '''Cache entry Time To Live for decorated callable.'''

  _keyFunc: Optional[Callable]
  '''Key creation function.'''

  _tags: Sequence[str]
  '''Cache entry tags for decorated callable.'''

  def __init__(
    self,
    frontend: 'Hermes',
    callable: Callable,
    *,
    ttl: Optional[int] = None,
    key: Optional[Callable] = None,
    tags: Sequence[str] = (),
  ):
    self._frontend = frontend
    self._ttl      = ttl
    self._keyFunc  = key
    self._tags     = tags

    self._callable     = callable
    self._isDescriptor = inspect.ismethoddescriptor(callable)
    self._isMethod     = inspect.ismethod(callable)

    # preserve ``__name__``, ``__doc__``, etc
    functools.update_wrapper(self, callable)

  def _load(self, key):
    if self._tags:
      tagMap = self._frontend.backend.load(map(self._frontend.mangler.nameTag, self._tags))
      if len(tagMap) != len(self._tags):
        return None
      else:
        key += ':' + self._frontend.mangler.hashTags(tagMap)

    return self._frontend.backend.load(key)

  def _save(self, key, value):
    if self._tags:
      namedTags   = tuple(map(self._frontend.mangler.nameTag, self._tags))
      tagMap      = self._frontend.backend.load(namedTags)
      missingTags = set(namedTags) - set(tagMap.keys())
      if missingTags:
        missingTagMap = self._frontend.mangler.mapTags(missingTags)
        self._frontend.backend.save(mapping = missingTagMap, ttl = None)
        tagMap.update(missingTagMap)
        assert len(self._tags) == len(tagMap)

      key += ':' + self._frontend.mangler.hashTags(tagMap)

    ttl = self._ttl if self._ttl is not None else self._frontend.ttl

    return self._frontend.backend.save({key: value}, ttl = ttl)

  def _remove(self, key):
    if self._tags:
      tagMap = self._frontend.backend.load(map(self._frontend.mangler.nameTag, self._tags))
      if len(tagMap) != len(self._tags):
        return
      else:
        key += ':' + self._frontend.mangler.hashTags(tagMap)

    self._frontend.backend.remove(key)

  def _key(self, *args, **kwargs):
    keyFunc = self._keyFunc or self._frontend.mangler.nameEntry
    return keyFunc(self._callable, *args, **kwargs)

  def invalidate(self, *args, **kwargs):
    '''
    Invalidate the cache entry.

    Invalidated entry corresponds to the wrapped callable called with
    given ``args`` and ``kwargs``.
    '''

    self._remove(self._key(*args, **kwargs))

  def __call__(self, *args, **kwargs):
    '''Get the value of the wrapped callable.'''

    key   = self._key(*args, **kwargs)
    value = self._load(key)
    if value is None:
      with self._frontend.backend.lock(key):
        # it's better to read twice than lock every read
        value = self._load(key)
        if value is None:
          value = self._callable(*args, **kwargs)
          self._save(key, value)

    return value

  def __get__(self, instance, type):
    '''
    Implements non-data descriptor protocol.

    The invocation happens only when instance method is decorated,
    so we can distinguish between decorated ``types.MethodType`` and
    ``types.FunctionType``. Python class declaration mechanics prevent
    a decorator from having awareness of the class type, as the
    function is received by the decorator before it becomes an
    instance method.

    How it works::

      cache = hermes.Hermes()

      class Model:

        @cache
        def calc(self):
          return 42

      m = Model()
      m.calc

    Last attribute access results in the call, ``calc.__get__(m, Model)``,
    where ``calc`` is instance of :class:`Cached` which decorates the
    original ``Model.calc``.

    Note, initially :class:`Cached` is created on decoration per
    class method, when class type is created by the interpreter, and
    is shared among all instances. Later, on attribute access, a copy
    is returned with bound ``_callable``, just like ordinary Python
    method descriptor works.

    For more details, `descriptor-protocol
    <http://docs.python.org/3/howto/descriptor.html#descriptor-protocol>`_.
    '''

    if instance is not None and self._isDescriptor:
      return self._copy(self._callable.__get__(instance, type))  # type: ignore[attribute-error]
    elif instance is not None and not self._isMethod:
      return self._copy(types.MethodType(self._callable, instance))
    else:
      return self

  def _copy(self, callable):
    '''
    Create a shallow copy of self with ``_callable``
    replaced to given instance.
    '''

    boundCached           = object.__new__(self.__class__)
    boundCached.__dict__  = self.__dict__.copy()
    boundCached._callable = callable
    return boundCached


class CachedCoro(Cached):
  '''
  Cache-point wrapper for coroutine functions.

  The implementation uses the default thread pool of ``asyncio`` to
  execute synchronous functions of the cache backend, and manage their
  (distributed) locks.
  '''

  async def _run(self, fn, *args, **kwargs) -> Coroutine:
    ''''
    Run run given function or coroutine function.

    If ``fn`` is a coroutine function it's called and awaited.
    Otherwise it's run in the thread pool.
    '''

    if inspect.iscoroutinefunction(fn):
      return await fn(*args, **kwargs)

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, functools.partial(fn, *args, **kwargs))

  async def invalidate(self, *args, **kwargs):
    '''
    Invalidate the cache entry.

    Invalidated entry corresponds to the wrapped coroutine function
    called with given ``args`` and ``kwargs``.
    '''

    await self._run(super().invalidate, *args, **kwargs)

  async def __call__(self, *args, **kwargs):
    '''Get the value of the wrapped coroutine function's coroutine.'''

    key = self._key(*args, **kwargs)
    value = await self._run(self._load, key)
    if value is None:
      lock = self._frontend.backend.lock(key)
      await self._run(lock.acquire)
      try:
        value = await self._run(self._load, key)
        if value is None:
          value = await self._callable(*args, **kwargs)
          await self._run(self._save, key, value)
      finally:
        await self._run(lock.release)

    return value


def cachedfactory(frontend: 'Hermes', fn, **kwargs) -> Cached:
  '''
  Create a cache-point object from the callable.

  :argument frontend:
    Cache frontend instance.
  :argument fn:
    Must be coroutine function, callable or method descriptor.
  '''

  isdescr = inspect.ismethoddescriptor(fn)
  if (
    inspect.iscoroutinefunction(fn)
    or isdescr and inspect.iscoroutinefunction(getattr(fn, '__func__', None))
  ):
    return CachedCoro(frontend, fn, **kwargs)
  elif callable(fn) or isdescr:
    return Cached(frontend, fn, **kwargs)
  else:
    raise HermesError(
      'First positional argument must be coroutine function, callable or method descriptor'
    )


class Hermes:
  '''
  Cache façade.

  :argument backend:
    Class or instance of cache backend. If a class is passed, keyword
    arguments of passed to :obj:`Hermes` constructor will be bypassed
    to the class' constructor.

    If the argument is omitted no-op backend will be be used.
  :argument mangler:
    Optional, typically of a subclass, mangler instance.
  :argument cachedfactory:
    Optional, a cache-point factory for functions and coroutines.
  :argument ttl:
    Default cache entry time-to-live.

  Usage::

    import hermes.backend.redis


    cache = hermes.Hermes(
      hermes.backend.redis.Backend, ttl = 600, host = 'localhost', db = 1
    )

    @cache
    def foo(a, b):
      return a * b

    class Example:

      @cache(tags = ('math', 'power'), ttl = 1200)
      def bar(self, a, b):
        return a ** b

      @cache(
        tags = ('math', 'avg'),
        key = lambda fn, *args, **kwargs: 'avg:{0}:{1}'.format(*args),
      )
      def baz(self, a, b):
        return (a + b) / 2.0

    print(foo(2, 333))

    example = Example()
    print(example.bar(2, 10))
    print(example.baz(2, 10))

    foo.invalidate(2, 333)
    example.bar.invalidate(2, 10)
    example.baz.invalidate(2, 10)

    cache.clean(['math']) # invalidate entries tagged 'math'
    cache.clean()         # flush cache

  '''

  backend: AbstractBackend
  '''Cache backend.'''

  mangler: Mangler
  '''Key manager responsible for creating keys, hashing and serialisation.'''

  cachedfactory: Callable[..., Cached]
  '''Cache-point callable object factory.'''

  ttl: int
  '''Default cache entry time-to-live.'''

  def __init__(
    self,
    backend: Union[Type[AbstractBackend], AbstractBackend] = AbstractBackend,
    *,
    mangler: Optional[Mangler] = None,
    cachedfactory: Callable[..., Cached] = cachedfactory,
    ttl: int = 3600,
    **backendconf
  ):
    self.ttl = ttl

    mangler = mangler or Mangler()
    assert isinstance(mangler, Mangler)
    self.mangler = mangler

    if isinstance(backend, AbstractBackend):
      if backendconf:
        warnings.warn('Backend options ignored because backend instance is passed')

      self.backend = backend
    elif isinstance(backend, type) and issubclass(backend, AbstractBackend):
      self.backend = backend(self.mangler, **backendconf)
    else:
      raise HermesError('Expected class or instance of AbstractBackend')  # type: ignore

    assert callable(cachedfactory)
    self.cachedfactory = cachedfactory

  def __call__(
    self,
    *args,
    ttl: Optional[int] = None,
    tags: Sequence[str] = (),
    key: Optional[Callable] = None,
  ):
    '''
    Wrap the callable in a cache-point instance.

    Decorator that caches method or function result. The following key
    arguments are optional:

    Bare decorator, ``@cache``, is supported as well as a call with
    keyword arguments ``@cache(ttl = 7200)``.

    :argument ttl:
      Seconds until entry expiration, otherwise instance's default
      is used.
    :argument tags:
      Cache entry tag list.
    :argument key:
      Lambda that provides custom key, otherwise
      :obj:`Mangler.nameEntry` is used.
    '''

    if args:
      # @cache
      return self.cachedfactory(self, args[0])
    else:
      # @cache()
      return functools.partial(self.cachedfactory, self, ttl = ttl, tags = tags, key = key)

  def clean(self, tags: Sequence[str] = ()):
    '''
    Clean all, or tagged with given tags, cache entries.

    :argument tags:
      If this argument is omitted the call flushes all cache entries,
      otherwise only the entries tagged by given tags are flushed.
    '''

    if tags:
      self.backend.remove(map(self.mangler.nameTag, tags))
    else:
      self.backend.clean()


class HermesError(Exception):
  '''Generic Hermes error.'''
