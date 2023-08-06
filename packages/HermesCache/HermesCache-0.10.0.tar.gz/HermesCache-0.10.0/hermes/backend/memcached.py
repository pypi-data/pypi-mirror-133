import time
from typing import Any, Dict, Iterable, Optional, Union

import pymemcache

from . import AbstractBackend, AbstractLock


__all__ = 'Backend',


class Lock(AbstractLock):
  '''Key-aware distributed lock.'''

  client: pymemcache.PooledClient
  '''Memcached client.'''

  timeout: int
  '''
  Maximum TTL of lock, can be up to 30 days, otherwise memcached will
  treated it as a UNIX timestamp of an exact date.
  '''

  sleep: float
  '''Amount of time to sleep per ``while True`` iteration when waiting.'''

  def __init__(
    self, key: str, client: pymemcache.PooledClient, *, sleep: float = 0.1, timeout: int = 900
  ):
    super().__init__(key)

    self.client  = client
    self.sleep   = sleep
    self.timeout = timeout

  def acquire(self, wait = True):
    while True:
      if self.client.add(self.key, 'locked', self.timeout, noreply = False):
        return True
      elif not wait:
        return False
      else:
        time.sleep(self.sleep)

  def release(self):
    self.client.delete(self.key)


class Backend(AbstractBackend):
  '''Memcached backend implementation.'''

  client: pymemcache.PooledClient
  '''Memcached client.'''

  _lockconf: dict
  '''Lock config.'''

  def __init__(
    self,
    mangler,
    *,
    server: str = 'localhost:11211',
    lockconf: Optional[dict] = None,
    **kwargs,
  ):
    self.mangler = mangler

    # Memcached client creates a pool that connects lazily
    self.client = pymemcache.PooledClient(server, **kwargs)

    self._lockconf = lockconf or {}

  def lock(self, key) -> Lock:
    return Lock(self.mangler.nameLock(key), self.client, **self._lockconf)

  def save(self, mapping: Dict[str, Any], *, ttl: Optional[int] = None):
    mapping = {k: self.mangler.dumps(v) for k, v in mapping.items()}
    self.client.set_multi(mapping, ttl if ttl is not None else 0)

  def load(self, keys: Union[str, Iterable[str]]) -> Optional[Union[Any, Dict[str, Any]]]:
    if isinstance(keys, str):
      value = self.client.get(keys)
      if value is not None:
        value = self.mangler.loads(value)
      return value
    else:
      return {k: self.mangler.loads(v) for k, v in self.client.get_multi(tuple(keys)).items()}

  def remove(self, keys: Union[str, Iterable[str]]):
    if isinstance(keys, str):
      keys = (keys,)

    self.client.delete_multi(keys)

  def clean(self):
    self.client.flush_all()
