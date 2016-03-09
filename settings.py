from kazoo.client import KazooClient
from kazoo.recipe.queue import LockingQueue

ZK_CLIENT = KazooClient()
ZK_CLIENT.start()


DATABASE_QUEUE = LockingQueue(ZK_CLIENT, '/database_queue')
