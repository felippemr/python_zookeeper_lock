import json
import logging
from kazoo import exceptions

logging.basicConfig()
LOG = logging.getLogger("BaseWorker")
LOG.setLevel(logging.INFO)

KEEP_WORKING = True


def base_worker(queue, function, lock_manager):
    LOG.info("Worker Started!")
    while KEEP_WORKING:
        message = parse_message(queue.get())
        if message['name'] is not None:
            try:
                with lock_manager.get(message['name']):
                    if queue.consume():
                        function(message)
            except exceptions.LockTimeout:
                LOG.info("LockTimeout on {}".format(message['name']))
            except Exception as e:
                LOG.warn("Exception: {}".format(e))
    LOG.info("Worker stoped!")


def parse_message(message):
    return json.loads(message.decode("utf-8"))
