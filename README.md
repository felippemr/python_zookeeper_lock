Lab to test zookeeper locks and queues

Requirements
============

* Zookeeper >= 3.4
* Python >= 3.4
* AMPQ >= 3.5.4

Setting up local environment
=============================

    $ mkvirtualenv python_zk_lab
    $ workon python_zk_lab
    $ make pip


Testing
=======

    $ zkServer start
    $ rabbitmq-server
    $ nameko run start_queues
    $ nameko shell
    >>> n.rpc.database_service.create_database(engine="mysql", name="teste999991", cpu="1", mem="2048")
