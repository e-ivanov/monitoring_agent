#!/usr/bin/env python
# -*- coding: utf-8 -*-

from version_checker import build_config
import os.path

import logging

class Config:
    def __init__(self):
        self.__config_file=r'main_config.txt'
        # self.__filehandle=open(self.__config_file,'w')
        self.__configParser = build_config()
        self.__configParser.read(self.__config_file)

    def set(self, section, option, value):
        self.__configParser.set(section, option, value)


    def get(self, section, option):
        return self.__configParser.get(section, option)
    def getFloat(self, section, option):
        return self.__configParser.getfloat(section, option)

    def save(self):
        with open(self.__config_file, 'w') as configfile:
            self.__configParser.write(configfile)

