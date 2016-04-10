import json
import logging
import sys
import multiprocessing
from contextlib import contextmanager
from kazoo import exceptions
from kazoo.client import KazooClient
from kazoo.recipe.queue import LockingQueue



def worker(*args, name):
    process = multiprocessing.Process(
            target=_work, args=args, name=name, daemon=True
        )
    process.start()
    process.join()


def _work(queue_name, function, resource_name, lock_timeout=10):
    logger = setup_logger(queue_name)
    logger.info("Worker Started!")

    zookeeper_client = get_zookeeper_client()
    queue = LockingQueue(zookeeper_client, queue_name)

    while True:
        try:
            message = get_next_message(queue)
        except Exception as e:
            logger.exception(
                "Error while retrieving message from queue: {}".format(e)
            )

        try:
            with get_resource_lock(
                resource_name, zookeeper_client, message['name'],
                timeout=lock_timeout
            ):
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


def setup_logger(queue_name):
    sys.stderr = open('logs/{}.txt'.format(queue_name), 'w')

    logger = multiprocessing.log_to_stderr()
    logger.setLevel(logging.INFO)
    return logger


def get_zookeeper_client():
    zookeeper_client = KazooClient()
    zookeeper_client.start()
    return zookeeper_client


def get_next_message(queue):
    return json.loads(queue.get().decode("utf-8"))


@contextmanager
def get_resource_lock(name, zookeeper_client, resource_id, timeout=60.0):
    lock = zookeeper_client.Lock(
        "/{}".format(name), "{}".format(resource_id)
    )
    try:
        lock.acquire(blocking=True, timeout=timeout)
        yield lock
    finally:
        lock.release()

