#!/usr/bin/env python
# -*- coding: utf-8 -*-
import jsonpickle
import json

import os.path
import pickle
import logging

class Config:
    def __init__(self):
        entry = None
        if os.path.isfile('config.dat'):
            with open('config.dat', 'rb') as f:
                entry = pickle.load(f)
        else:
            logging.error("Няма наличен файл config.dat!")
        if entry is not None:
            data = json.loads(entry)
            for key, value in data.items():
                setattr(self, key, value)
        else:
            logging.error("Неуспешен опит за десериализиране на конфигурационните данни!")


    def getCollectionInterval(self):
        if self.collectionInterval == 0:
            return 60
        return self.collectionInterval

    def setCollectionInterval(self, interval):
        self.collectionInterval = interval

    def getServerId(self):
        return self.serverId

    def setServerId(self,serverId):
        self.serverId = serverId


    def __getstate__(self):
        state = {"collectionInterval": self.collectionInterval,
                 "serverId": self.serverId}
        return state

    def toJSON(self):

        return jsonpickle.encode(self, unpicklable=False)