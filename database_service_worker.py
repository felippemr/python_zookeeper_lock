import json
import logging
import settings
from time import sleep
from kazoo import exceptions

logging.basicConfig()
LOG = logging.getLogger("DatabaseServiceWorker")
LOG.setLevel(logging.DEBUG)

KEEP_WORKING = True


def work():
    LOG.info("Worker Started!")
    while KEEP_WORKING:
        message = parse_message(settings.DATABASE_QUEUE.get())
        if message['name'] is not None:
            try:
                with settings.DATABASE_RESOURCE_MANAGER.get(message['name']):
                    if settings.DATABASE_QUEUE.consume():
                        create_database(message)
            except exceptions.LockTimeout:
                LOG.info("LockTimeout on {}".format(message['name']))
            except Exception as e:
                LOG.warn("Exception: {}".format(e))


def parse_message(message):
    return json.loads(message.decode("utf-8"))


def create_database(message):
    sleep(30)
    LOG.info("Database {} succesfully created!".format(message['name']))


if __name__ == '__main__':
    try:
        work()
    except KeyboardInterrupt:
        LOG.info("Shuting down worker...")
        KEEP_WORKING = False
