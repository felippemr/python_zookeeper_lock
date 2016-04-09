import json
from kazoo import exceptions

KEEP_WORKING = True


def base_worker(logger, queue, function, lock_manager):
    logger.info("Worker Started!")
    while KEEP_WORKING:
        message = parse_message(queue.get())
        if message['name'] is not None:
            try:
                with lock_manager.get(message['name']):
                    if queue.consume():
                        function(message)
            except exceptions.LockTimeout:
                logger.info("LockTimeout on {}".format(message['name']))
            except Exception as e:
                logger.warn("Exception: {}".format(e))
    logger.info("Worker stoped!")


def parse_message(message):
    return json.loads(message.decode("utf-8"))
