Lab to test zookeeper locks and queues

Requirements
============

* Zookeeper >= 3.4
* Python >= 3.4

Setting up local environment
=============================

    $ zkServer start
    $ mkvirtualenv python_zk_lab
    $ workon python_zk_lab
    $ make pip


Testing
=======

    $ python start_queues.py --bind 127.0.0.1:9001
    $ python
    >>> from pulsar.apps.rpc.jsonrpc import JsonProxy
    >>> import asyncio
    >>> p = JsonProxy('http://127.0.0.1:9001')
    >>> a = p.database_manager.create_database('mysql', 'test', '1', '2048')
    >>> task = asyncio.async(a)
    >>> task.loop = asyncio.get_event_loop()
    >>> loop = asyncio.get_event_loop()
    >>> loop.run_until_complete(task)
