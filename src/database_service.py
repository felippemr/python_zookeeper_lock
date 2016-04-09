import json
import logging
import settings
from nameko.rpc import rpc
from nameko.runners import ServiceRunner

logging.basicConfig(
    filename='logs/database_rpc_service.txt',
    level=logging.INFO
)
LOG = logging.getLogger("DatabaseEnQueueService")



class DatabaseService(object):
    name = "database_service"

    @rpc
    def create_database(self, engine, name, cpu, mem):
        call_args = bytes(json.dumps(
            {"engine": engine, "name": name, "cpu": cpu, "mem": mem}
        ), 'utf-8')
        LOG.info("Args Converted")

        settings.CREATE_DATABASE_QUEUE.put(call_args)
        LOG.info("Queue updated")

        return "Create request sent to queue"

    @rpc
    def destroy_database(self, engine, name, cpu, mem):
        call_args = bytes(json.dumps(
            {"engine": engine, "name": name, "cpu": cpu, "mem": mem}
        ), 'utf-8')
        LOG.info("Args Converted")

        settings.DESTROY_DATABASE_QUEUE.put(call_args)
        LOG.info("Queue updated")

        return "Destroy request sent to queue"

def main():
    config = {
        '_log': LOG,
        'AMQP_URI': 'amqp://guest:guest@localhost'
    }
    runner = ServiceRunner(config)
    runner.add_service(DatabaseService)

    runner.start()

    try:
        runner.wait()
    except (KeyboardInterrupt, SystemExit):
        runner.kill()

if __name__ == '__main__':
    main()
