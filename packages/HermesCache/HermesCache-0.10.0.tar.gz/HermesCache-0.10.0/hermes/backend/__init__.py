from typing import TYPE_CHECKING, Any, Dict, Iterable, Optional, Union


if TYPE_CHECKING:
  from .. import Mangler  # @UnusedImport


__all__ = 'AbstractBackend',


class AbstractLock:
  '''
  Base locking class. Implements context manger protocol. Mocks
  ``acquire`` and ``release`` i.e. it always acquires.
  '''

  key: str
  '''Implementation may be key-aware.'''

  def __init__(self, key: str):
    self.key = key

  def __enter__(self):
    '''Enter context manager by acquiring the distributed lock.'''

    self.acquire()

  def __exit__(self, type, value, traceback):
    '''Exit context manager by releasing the distributed lock.'''

    self.release()

  def acquire(self, wait = True) -> bool:
    '''
    Acquire distributed lock.

    :argument wait: Whether to wait for the lock.
    :return: Whether the lock was acquired.
    '''

    return True

  def release(self):
    '''Release distributed lock.'''


class AbstractBackend:
  '''Base backend class. It's also the no-op implementation.'''

  mangler: 'Mangler'
  '''Key manager responsible for creating keys, hashing and serialisation.'''

  def __init__(self, mangler: 'Mangler'):
    self.mangler = mangler

  def lock(self, key: str) -> AbstractLock:
    '''Create lock object for the key.'''

    return AbstractLock(self.mangler.nameLock(key))

  def save(self, mapping: Dict[str, Any], *, ttl: Optional[int] = None):
    '''
    Save cache entry.

    :argument key: Cache entry key.
    :argument value: Cache entry value.
    :argument mapping: Alternative to ``key`` and ``value`` for a bulk save.
    :argument ttl: Cache entry time-to-live .
    '''

  def load(self, keys: Union[str, Iterable[str]]) -> Optional[Union[Any, Dict[str, Any]]]:
    '''
    Load cache entry(ies).

    Note, when handling a multiple key call, absent value keys
    should be excluded from resulting dictionary.
    '''

    return None if isinstance(keys, str) else {}

  def remove(self, keys: Union[str, Iterable[str]]):
    '''Remove given keys.'''

  def clean(self):
    '''Purge the backend storage.'''
