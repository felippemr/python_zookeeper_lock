import json
import logging
import settings
from nameko.rpc import rpc

logging.basicConfig()
LOG = logging.getLogger("DatabaseQueueService")
LOG.setLevel(logging.DEBUG)


class DatabaseService(object):
    name = "database_service"

    @rpc
    def create_database(self, engine, name, cpu, mem):
        call_args = bytes(json.dumps(
            {"engine": engine, "name": name, "cpu": cpu, "mem": mem}
        ), 'utf-8')
        LOG.debug("Args Converted")

        settings.DATABASE_QUEUE.put(call_args)
        LOG.debug("Queue updated")

        return "Create request sent to queue"
