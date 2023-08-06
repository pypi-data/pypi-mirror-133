import time
from typing import Any, Dict, Iterable, Optional, Union

import redis

from . import AbstractBackend, AbstractLock


__all__ = 'Backend',


class Lock(AbstractLock):
  '''
  Key-aware distributed lock. "Distributed" is in sense of clients,
  not Redis instances. Implemented as described in `Correct
  implementation with a single instance <lock_>`_, but without
  setting unique value to the lock entry and later checking it, because
  it is expected for a cached function to complete before lock timeout.

  .. _lock: http://redis.io/topics/distlock#correct-implementation-with-a-single-instance
  '''

  client: redis.StrictRedis
  '''Redis client.'''

  timeout: int
  '''Maximum TTL of lock.'''

  sleep: float
  '''Amount of time to sleep per ``while True`` iteration when waiting.'''

  def __init__(
    self, key: str, client: redis.StrictRedis, *, sleep: float = 0.1, timeout: int = 900
  ):
    super().__init__(key)

    self.client  = client
    self.sleep   = sleep
    self.timeout = timeout

  def acquire(self, wait = True):
    while True:
      if self.client.set(self.key, 'locked', nx = True, ex = self.timeout):
        return True
      elif not wait:
        return False
      else:
        time.sleep(self.sleep)

  def release(self):
    self.client.delete(self.key)


class Backend(AbstractBackend):
  '''Redis backend implementation.'''

  client: redis.StrictRedis
  '''Redis client.'''

  _lockconf: dict
  '''Lock config.'''

  def __init__(
    self,
    mangler,
    *,
    host: str = 'localhost',
    password: Optional[str] = None,
    port: int = 6379,
    db: int = 0,
    lockconf: Optional[dict] = None,
    **kwargs
  ):
    super().__init__(mangler)

    # Redis client creates a pool that connects lazily
    self.client = redis.StrictRedis(host, port, db, password, **kwargs)

    self._lockconf = lockconf or {}

  def lock(self, key: str) -> Lock:
    return Lock(self.mangler.nameLock(key), self.client, **self._lockconf)

  def save(self, mapping: Dict[str, Any], *, ttl: Optional[int] = None):
    mapping = {k: self.mangler.dumps(v) for k, v in mapping.items()}

    if not ttl:
      self.client.mset(mapping)
    else:
      pipeline = self.client.pipeline()
      for k, v in mapping.items():
        pipeline.setex(k, ttl, v)
      pipeline.execute()

  def load(self, keys: Union[str, Iterable[str]]) -> Optional[Union[Any, Dict[str, Any]]]:
    if isinstance(keys, str):
      value = self.client.get(keys)
      if value is not None:
        value = self.mangler.loads(value)
      return value
    else:
      keys = tuple(keys)
      return {
        k: self.mangler.loads(v)
        for k, v in zip(keys, self.client.mget(keys))
        if v is not None
      }

  def remove(self, keys: Union[str, Iterable[str]]):
    if isinstance(keys, str):
      keys = (keys,)

    self.client.delete(*keys)

  def clean(self):
    self.client.flushdb()
