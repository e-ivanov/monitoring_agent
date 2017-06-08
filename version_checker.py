#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys



def build_config():
     if (sys.version_info > (3, 0)):
         import configparser
         return configparser.ConfigParser()
     else:
         import ConfigParser
         return ConfigParser.RawConfigParser()
