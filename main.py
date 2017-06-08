#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging
from multiprocessing import Process
from multiprocessing.managers import BaseManager
import jsonpickle
import pika
from version_checker import build_config


from PSUtilsStatProvider import PSUtilStatProvider
from ServerData import ServerData
from Config import Config
from web.web import start_app

properties = pika.BasicProperties(content_type='application/json')
logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

credentials = pika.PlainCredentials('admin', 'admin')
connection = None


# configParser = ConfigParser.RawConfigParser()
configParser = build_config()
configFilePath = r'ip_config.txt'
configParser.read(configFilePath)
rabbit_address = configParser.get("ip", "rabbit_address")

SERVER_ID = -1



class CollectionManger(BaseManager):
    pass

CollectionManger.register("Config", Config)

def connect_to_rabbit():
    global connection, channel, config, rabbit_address
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_address, credentials=credentials))
        channel = connection.channel()
        channel.exchange_declare(exchange='server_data', type='direct', auto_delete=False)
        channel.exchange_declare(exchange='server_data_stat', type='topic', auto_delete=False)
        logger.info("Осъществена е успешна връзка с RabbitMQ");
    except:
        logger.error("Грешка при опита за връзка с RabbitMQ.")

def collect_perf_info(config):
    global channel
    global server_data
    global connection
    global rabbit_address
    while True:
        try:
            server_data.refreshData()
            s = jsonpickle.encode(server_data, unpicklable=False)
            logger.info(s)
            if connection is None or connection.is_closed:
                logger.info("Опит за реинициализиране на връзката с RabbitMQ")
                rabbit_address = configParser.get("ip", "rabbit_address")
                connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_address, credentials=credentials))
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
    m = CollectionManger()
    m.start()
    config = m.Config()
    psutilstat = PSUtilStatProvider(m.Config())
    server_data = ServerData(psutilstat, m.Config())
    flaskProcess = Process(name="flaskApp", target=start_app, args=(config, configParser.get("ip", "flask_bind_address"),))
    flaskProcess.start()
    logger.info("Started Flask process")
    connect_to_rabbit()
    collect_perf_info(config)



