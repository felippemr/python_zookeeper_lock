import logging
from time import sleep
from base import base_worker
import settings


def destroy_database(message):
    LOG.info("Destroying Database...")
    sleep(10)
    LOG.info("Database {} succesfully destroyed!".format(message['name']))


if __name__ == '__main__':
    logging.basicConfig(
        filename='logs/destroy_database_worker.txt',
        level=logging.INFO
    )
    LOG = logging.getLogger("DestroyDatabaseServiceWorker")

    try:
        base_worker(
            logger=LOG,
            queue=settings.DESTROY_DATABASE_QUEUE,
            function=destroy_database,
            lock_manager=settings.DATABASE_RESOURCE_MANAGER
        )
    except (KeyboardInterrupt, SystemExit):
        LOG.info("Shuting down worker...")
        KEEP_WORKING = False
