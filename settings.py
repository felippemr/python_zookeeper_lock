from kazoo.client import KazooClient
from kazoo.recipe.queue import LockingQueue
import resource

ZK_CLIENT = KazooClient()
ZK_CLIENT.start()


DATABASE_QUEUE = LockingQueue(ZK_CLIENT, '/database_queue')
DATABASE_RESOURCE_MANAGER = resource.Resource('database')
