import json
import logging
import sys
import multiprocessing
from contextlib import contextmanager
from kazoo import exceptions
from kazoo.client import KazooClient
from kazoo.recipe.queue import LockingQueue


class Resource(object):
    def __init__(self, name, zookeeper_client):
        self._zookeeper_client = zookeeper_client
        self._name = name
    @contextmanager
    def get(self, resource_id, timeout=60.0):
        lock = self._zookeeper_client.Lock(
            "/{}".format(self._name), "{}".format(resource_id)
        )
        try:
            lock.acquire(blocking=True, timeout=timeout)
            yield lock
        finally:
            lock.release()



def worker(*args, name):
    process = multiprocessing.Process(
            target=_work, args=args, name=name, daemon=True
        )
    process.start()
    process.join()

def _work(queue_name, function, resource_name, lock_timeout=10):
    sys.stderr = open('logs/{}.txt'.format(queue_name), 'w')

    zookeeper_client = KazooClient()
    zookeeper_client.start()
    queue = LockingQueue(zookeeper_client, queue_name)

    resource_manager = Resource(resource_name, zookeeper_client)

    logger = multiprocessing.log_to_stderr()
    logger.setLevel(logging.INFO)
    logger.info("Worker Started!")

    while True:
        try:
            message = json.loads(queue.get().decode("utf-8"))
            logger.info("Processing message: {}".format(message))
        except Exception as e:
            logger.exception(
                "Error while retrieving message from queue: {}".format(e)
            )

        try:
            with resource_manager.get(message['name'], timeout=lock_timeout):
                if queue.consume():
                    try:
                        function(message, logger)
                    except Exception as e:
                        logger.exception(
                            "Function raised exception: {}".format(e)
                        )
        except exceptions.LockTimeout:
            logger.info("LockTimeout on {}".format(message['name']))
        except Exception as e:
            logger.exception("Exception: {}".format(e))
