import logging
import settings
from time import sleep
from base import base_worker


def create_database(message):
    LOG.info("Creating Database...")
    sleep(30)
    LOG.info("Database {} succesfully created!".format(message['name']))


if __name__ == '__main__':
    logging.basicConfig(
        filename='logs/create_database_worker.txt',
        level=logging.INFO
    )
    LOG = logging.getLogger("CreateDatabaseServiceWorker")

    try:
        base_worker(
            logger=LOG,
            queue=settings.CREATE_DATABASE_QUEUE,
            function=create_database,
            lock_manager=settings.DATABASE_RESOURCE_MANAGER
        )
    except (KeyboardInterrupt, SystemExit):
        LOG.info("Shuting down worker...")
        KEEP_WORKING = False
