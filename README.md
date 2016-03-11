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
    $ python database_service_worker.py (you can start as many workers as you want)
