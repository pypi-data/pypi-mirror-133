import asyncio
import heapq
import threading
import time
import weakref
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

from . import AbstractBackend, AbstractLock


__all__ = 'AsyncBackend', 'Backend'


class Lock(AbstractLock):
  '''Key-unaware reentrant thread lock.'''

  _lock: threading.RLock
  '''Threading lock instance.'''

  def __init__(self, key = None):
    self._lock = threading.RLock()

  def acquire(self, wait = True):
    '''Acquire the ``RLock``.'''

    return self._lock.acquire(wait)

  def release(self):
    '''Release the ``RLock``.'''

    self._lock.release()


class BaseBackend(AbstractBackend):
  '''Base dictionary backend without key expiration.'''

  cache: dict
  '''A ``dict`` used to store cache entries.'''

  def __init__(self, mangler):
    super().__init__(mangler)

    self.cache = {}

  def save(self, mapping: Dict[str, Any], *, ttl: Optional[int] = None):
    self.cache.update({k: self.mangler.dumps(v) for k, v in mapping.items()})

  def load(self, keys: Union[str, Iterable[str]]) -> Optional[Union[Any, Dict[str, Any]]]:
    if isinstance(keys, str):
      value = self.cache.get(keys, None)
      if value is not None:
        value = self.mangler.loads(value)
      return value
    else:
      return {k: self.mangler.loads(self.cache[k]) for k in keys if k in self.cache}

  def remove(self, keys: Union[str, Iterable[str]]):
    if isinstance(keys, str):
      keys = (keys,)

    for key in keys:
      self.cache.pop(key, None)

  def clean(self):
    self.cache.clear()

  def dump(self) -> Dict[str, Any]:
    '''Dump the cache entries. Sorry, Barbara.'''

    return {k: self.mangler.loads(v) for k, v in self.cache.items()}


class Backend(BaseBackend):
  '''
  Simple in-process dictionary-based backend implementation.

  In-process in-memory cache without memory limit, but with
  expiration. Besides testing, it may be suitable for limited number of
  real-world use-cases with a priori small cached data.
  '''

  _lock: Lock
  '''Lock instance.'''

  _ttlHeap: list
  '''TTL heap used by the thread to remove the expired entries.'''

  _ttlWatchThread: threading.Thread
  '''An instance of TTL watcher thread.'''

  _ttlWatchSleep: float
  '''Seconds for the expiration watcher to sleep in the loop.'''

  _ttlWatchThreadRunning = False
  '''Run flag of the while-loop of the thread.'''

  def __init__(self, mangler, *, ttlWatchSleep: float = 1):
    super().__init__(mangler)

    self._lock = Lock()
    self._ttlHeap = []

    self._ttlWatchSleep = ttlWatchSleep
    self.startWatch()

  def lock(self, key: str) -> Lock:
    return self._lock

  def save(self, mapping: Dict[str, Any], *, ttl: Optional[int] = None):
    super().save(mapping, ttl = ttl)

    if ttl:
      for k in mapping:
        heapq.heappush(self._ttlHeap, (time.time() + ttl, k))

  def clean(self):
    # It touches the heap and needs to be synchronised
    with self._lock:
      super().clean()
      self._ttlHeap.clear()

  def startWatch(self):
    self._ttlWatchThread = threading.Thread(target = self._watchExpiry, daemon = True)
    self._ttlWatchThreadRunning = True
    self._ttlWatchThread.start()

  def stopWatch(self):
    '''Ask TTL watch thread to stop and join it.'''

    self._ttlWatchThreadRunning = False
    self._ttlWatchThread.join(2 * self._ttlWatchSleep)

  def dump(self) -> Dict[str, Any]:
    # It iterates the cache and needs to be synchronised
    with self._lock:
      return super().dump()

  def _watchExpiry(self):
    while self._ttlWatchThreadRunning:
      with self._lock:
        # May contain manually invalidated keys
        expiredKeys = []
        now = time.time()
        while self._ttlHeap and self._ttlHeap[0][0] < now:
          _, key = heapq.heappop(self._ttlHeap)
          expiredKeys.append(key)
        self.remove(expiredKeys)

      time.sleep(self._ttlWatchSleep)


class AsyncLock(AbstractLock):
  '''
  Key-aware asynchronous lock.

  Note that instances of this class are used for both synchronous and
  asynchronous cases. For asynchronous cases ``asyncio.Lock`` is used
  per key. When a synchronous callable is cached in an asynchronous
  application, synchronous code is by definition executed serially in
  single-threaded Python process running an ``asyncio`` IO loop. Hence,
  for synchronous code this class does nothing.

  The trick that makes it work for the both cases is that
  :class:`hermes.Cached` uses the context manager protocol, and
  :class:`hermes.CachedCoro` uses :obj:`.acquire` and
  :obj:`.release` directly.
  '''

  _lock: asyncio.Lock = None
  '''`Lock instance, created lazily on `.acquire` call.'''

  def __enter__(self):
    '''
    No-op context manager implementation.

    Used by :class:`hermes.Cached` for synchronous code.
    '''

  def __exit__(self, *args):
    '''
    No-op context manager implementation.

    Used by :class:`hermes.Cached` for synchronous code.
    '''

  async def acquire(self, wait = True):
    '''
    Acquire the asynchronous lock.

    Used by ``CachedCoro`` for asynchronous code.
    '''

    if not self._lock:
      self._lock = asyncio.Lock()

    if not wait and self._lock.locked():
      return False

    await self._lock.acquire()
    return True

  async def release(self):
    '''
    Release the asynchronous lock.

    Used by ``CachedCoro`` for asynchronous code.

    This method does not have to a coroutine itself, because underlying
    ``release`` is synchronous. But because :class:`hermes.CachedCoro`
    runs regular synchronous callables in a thread pool, and the thread
    won't have running IO loop, making this a coroutine lead to desired
    behaviour.
    '''

    self._lock.release()


class AsyncBackend(BaseBackend):
  '''
  Simple in-process dictionary-based backend for ``asyncio`` programs.

  For cache entries to expire according to their TTL,
  :meth:`.startWatch` must be awaited manually when the IO loop is
  already running.
  '''

  _lockMap: weakref.WeakValueDictionary
  '''`
  Mapping between cache keys and :class:`.AsyncLock` instances.

  ``WeakValueDictionary`` makes cleanup of released locks automatic.
  '''

  _ttlHeap: List[Tuple[float, str]]
  '''TTL heap used to remove the expired entries.'''

  _ttlWatchSleep: float
  '''Seconds for the expiration watcher to sleep in the loop.'''

  _ttlWatchTask: Optional[asyncio.Task] = None
  '''An instance of TTL watcher task, created by ``startWatch``.'''

  def __init__(self, mangler, *, ttlWatchSleep: float = 1):
    super().__init__(mangler)

    self._ttlWatchSleep = ttlWatchSleep

    self._lockMap = weakref.WeakValueDictionary()
    self._ttlHeap = []

  def lock(self, key: str) -> AsyncLock:
    try:
      return self._lockMap[key]
    except KeyError:
      return self._lockMap.setdefault(key, AsyncLock(key))

  def save(self, mapping: Dict[str, Any], *, ttl: Optional[int] = None):
    super().save(mapping, ttl = ttl)

    if ttl:
      for k in mapping:
        heapq.heappush(self._ttlHeap, (time.time() + ttl, k))

  def clean(self):
    super().clean()
    self._ttlHeap.clear()

  def startWatch(self):
    '''
    Start TTL watching task.

    It must be called when ``asyncio`` IO loop is running.
    '''

    self._ttlWatchTask = asyncio.get_event_loop().create_task(self._watchExpiry())

  def stopWatch(self):
    '''Stop TTL watching task.'''

    self._ttlWatchTask.cancel()

  async def _watchExpiry(self):
    while True:
      expiredKeys = []
      now = time.time()
      # The removal uses synchronous API so it's atomic for single-threaded
      # program by definition, and doesn't need any locking
      while self._ttlHeap and self._ttlHeap[0][0] < now:
        _, key = heapq.heappop(self._ttlHeap)
        expiredKeys.append(key)
      self.remove(expiredKeys)

      await asyncio.sleep(self._ttlWatchSleep)
