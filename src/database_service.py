import json
import logging
import settings
from nameko.rpc import rpc

logging.basicConfig()
LOG = logging.getLogger("DatabaseEnQueueService")
LOG.setLevel(logging.DEBUG)


class DatabaseService(object):
    name = "database_service"

    @rpc
    def create_database(self, engine, name, cpu, mem):
        call_args = bytes(json.dumps(
            {"engine": engine, "name": name, "cpu": cpu, "mem": mem}
        ), 'utf-8')
        LOG.debug("Args Converted")

        settings.CREATE_DATABASE_QUEUE.put(call_args)
        LOG.debug("Queue updated")

        return "Create request sent to queue"

    @rpc
    def destroy_database(self, engine, name, cpu, mem):
        call_args = bytes(json.dumps(
            {"engine": engine, "name": name, "cpu": cpu, "mem": mem}
        ), 'utf-8')
        LOG.debug("Args Converted")

        settings.DESTROY_DATABASE_QUEUE.put(call_args)
        LOG.debug("Queue updated")

        return "Destroy request sent to queue"
