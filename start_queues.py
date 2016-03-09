import json
import logging
# from settings import DATABASE_QUEUE
from pulsar import as_coroutine
from pulsar.apps import rpc, wsgi
from pulsar.utils.httpurl import JSON_CONTENT_TYPES
from kazoo.client import KazooClient
from kazoo.recipe.queue import LockingQueue

ZK_CLIENT = KazooClient()
ZK_CLIENT.start()


DATABASE_QUEUE = LockingQueue(ZK_CLIENT, '/database_queue')

logging.basicConfig()
LOG = logging.getLogger("QueueService")
LOG.setLevel(logging.DEBUG)


class RequestCheck:
    def __call__(self, request, name):
        data = yield from as_coroutine(request.body_data())
        assert(data['method'] == name)
        return True


class Database(rpc.JSONRPC):
    def rpc_create_database(self, request, engine, name, cpu, mem, ):
        LOG.debug("Request Initiated")

        call_args = bytes(json.dumps(
            {"engine": engine, "name": name, "cpu": cpu, "mem": mem}
        ), 'utf-8')
        LOG.debug("Args Converted")

        put = DATABASE_QUEUE.put(call_args)
        LOG.debug("Queue updated")

        return "Create {} with engine {}, and {} cpu and {} mem".format(
            name, engine, cpu, mem)


class Site(wsgi.LazyWsgi):
    def setup(self, environ):
        json_handler = rpc.PulsarServerCommands().putSubHandler('database_manager', Database())

        middleware = wsgi.Router(
            '/', post=json_handler, accept_content_types=JSON_CONTENT_TYPES)

        response = [wsgi.GZipMiddleware(200)]

        return wsgi.WsgiHandler(
            middleware=[wsgi.wait_for_body_middleware, middleware],
            response_middleware=response, async=True)


def server(callable=None, **params):
    return wsgi.WSGIServer(Site(), **params)


if __name__ == '__main__':
    server().start()
