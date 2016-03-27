import logging
from time import sleep
from base import base_worker
import settings

logging.basicConfig()
LOG = logging.getLogger("CreateDatabaseServiceWorker")
LOG.setLevel(logging.DEBUG)


def destroy_database(message):
    LOG.info("Destroying Database...")
    sleep(10)
    LOG.info("Database {} succesfully destroyed!".format(message['name']))


if __name__ == '__main__':
    try:
        base_worker(
            queue=settings.DESTROY_DATABASE_QUEUE,
            function=destroy_database,
            lock_manager=settings.DATABASE_RESOURCE_MANAGER
        )
    except KeyboardInterrupt:
        LOG.info("Shuting down worker...")
        KEEP_WORKING = False
