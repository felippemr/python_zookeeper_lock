import json
import errno
import logging
import settings
import eventlet
from eventlet import backdoor
from nameko.rpc import rpc
from nameko.runners import ServiceRunner

eventlet.monkey_patch(thread=False)

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
        'AMQP_URI': 'amqp://guest:guest@127.0.0.1:5672'
    }
    service_runner = ServiceRunner(config)
    service_runner.add_service(DatabaseService)

    service_runner.start()

    runnlet = eventlet.spawn(service_runner.wait)

    while True:
        try:
            runnlet.wait()
        except OSError as exc:
            if exc.errno == errno.EINTR:
                continue
            raise
        except KeyboardInterrupt:
            try:
                service_runner.stop()
            except KeyboardInterrupt:
                service_runner.kill()
        else:
            break

if __name__ == '__main__':
    main()
