from time import sleep
from base import worker


def create_database(message, logger):
    logger.info("Creating Database...")
    sleep(30)
    logger.info("Database {} succesfully created!".format(message['name']))


if __name__ == '__main__':

    worker(
        '/create_database_queue', create_database, 'database',
        name='create_database_worker'
    )
