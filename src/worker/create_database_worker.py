import logging
from time import sleep
import settings
from base import base_worker


logging.basicConfig()
LOG = logging.getLogger("CreateDatabaseServiceWorker")
LOG.setLevel(logging.DEBUG)


def create_database(message):
    LOG.info("Creating Database...")
    sleep(30)
    LOG.info("Database {} succesfully created!".format(message['name']))


if __name__ == '__main__':
    try:
        base_worker(
            queue=settings.CREATE_DATABASE_QUEUE,
            function=create_database,
            lock_manager=settings.DATABASE_RESOURCE_MANAGER
        )
    except KeyboardInterrupt:
        LOG.info("Shuting down worker...")
        KEEP_WORKING = False
