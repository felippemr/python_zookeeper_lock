from contextlib import contextmanager
import settings


class Resource(object):
    def __init__(self, name,):
        self._zookeeper_client = settings.ZK_CLIENT
        self._name = name

    @contextmanager
    def get(self, resource_id, timeout=60.0):
        lock = self._zookeeper_client.Lock(
            "/{}".format(self._name), "{}".format(resource_id))
        try:
            lock.acquire(blocking=True, timeout=timeout)
            yield
        finally:
            lock.release()
