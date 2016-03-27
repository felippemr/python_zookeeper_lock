from contextlib import contextmanager
from kazoo.client import KazooClient
from kazoo.recipe.queue import LockingQueue

ZK_CLIENT = KazooClient()
ZK_CLIENT.start()


class Resource(object):
    def __init__(self, name,):
        self._zookeeper_client = ZK_CLIENT
        self._name = name

    @contextmanager
    def get(self, resource_id, timeout=60.0):
        lock = self._zookeeper_client.Lock(
            "/{}".format(self._name), "{}".format(resource_id))
        try:
            lock.acquire(blocking=True, timeout=timeout)
            yield lock
        finally:
            lock.release()


DATABASE_RESOURCE_MANAGER = Resource('database')
CREATE_DATABASE_QUEUE = LockingQueue(ZK_CLIENT, '/create_database_queue')
DESTROY_DATABASE_QUEUE = LockingQueue(ZK_CLIENT, '/destroy_database_queue')
