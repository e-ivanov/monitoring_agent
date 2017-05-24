#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging
from multiprocessing import Process
from multiprocessing.managers import BaseManager
import jsonpickle
import pika

from PSUtilsStatProvider import PSUtilStatProvider
from ServerData import ServerData
from Config import Config
from web.web import startApp

properties = pika.BasicProperties(content_type='application/json')
logger = logging.getLogger("main");
logger.setLevel(logging.DEBUG);
logger.addHandler(logging.StreamHandler())

credentials = pika.PlainCredentials('admin', 'admin')
connection = None

psutilstat = PSUtilStatProvider()
server_data = ServerData(psutilstat)

class CollectionManger(BaseManager):
    pass

CollectionManger.register("Config", Config)

def connectToRabbit():
    global connection, channel, config
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', credentials=credentials))

        channel = connection.channel()
        channel.exchange_declare(exchange='server_data', type='direct', auto_delete=False)
        channel.exchange_declare(exchange='server_data_stat', type='topic', auto_delete=False)
        logger.info("Осъществена е успешна връзка с RabbitMQ");
    except:
        print connection
        logger.error("Грешка при опита за връзка с RabbitMQ.")

def collectPerfInfo(config):
    global channel
    global server_data
    global connection
    while True:
        try:
            server_data.refreshData()
            s = jsonpickle.encode(server_data, unpicklable=False)

            if connection is None or connection.is_closed:
                logger.info("Опит за реинициализиране на връзката с RabbitMQ")
                connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', credentials=credentials))
                channel = connection.channel()
                channel.exchange_declare(exchange='server_data', type='direct', auto_delete=False)
                channel.exchange_declare(exchange='server_data_stat', type='topic', auto_delete=False)

            channel.basic_publish(exchange='server_data',
                                  routing_key='server_stats',
                                  body=s,
                                  properties=properties)
            channel.basic_publish(exchange='server_data_stat',
                                  routing_key='server_'+str(config.getServerId()),
                                  body=s,
                                  properties=properties)
            logger.info("Успешно изпратено съобщение до RabbitMQ!");
            time.sleep(config.getCollectionInterval())
        except Exception as e:
            logger.error(e)
            logger.error("Грешка при опита за изпращане на съобщение до RabbitMQ" )


if __name__ == '__main__':
    m = CollectionManger();
    m.start()
    config = m.Config()
    flaskProcess = Process(name="flaskApp", target=startApp, args=(config,))
    flaskProcess.start()
    logger.info("Started Flask process")
    connectToRabbit()
    collectPerfInfo(config)



