#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, bcrypt

is_python_3 = sys.version_info > (3, 0)

def build_config():
     if (is_python_3):
         import configparser
         return configparser.ConfigParser()
     else:
         import ConfigParser
         return ConfigParser.RawConfigParser()

def read_input(data):
    if(is_python_3):
        return input(data)
    else:
        return raw_input(data)

def check_user_password(plaintext, hashed_pass):
    if(is_python_3):
        return bcrypt.checkpw(plaintext.encode('utf8'), hashed_pass)
    else:
        return bcrypt.checkpw(plaintext.encode('utf8'), hashed_pass.encode('utf8'))


