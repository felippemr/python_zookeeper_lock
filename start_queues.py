import json
import logging
from settings import DATABASE_QUEUE
from nameko.rpc import rpc

logging.basicConfig()
LOG = logging.getLogger("QueueService")
LOG.setLevel(logging.DEBUG)


class DatabaseService(object):
    name = "database_service"

    @rpc
    def create_database(self, engine, name, cpu, mem):
        call_args = bytes(json.dumps(
            {"engine": engine, "name": name, "cpu": cpu, "mem": mem}
        ), 'utf-8')
        LOG.debug("Args Converted")

        DATABASE_QUEUE.put(call_args)
        LOG.debug("Queue updated")

        return "Creat request sent to queue".format(name)
