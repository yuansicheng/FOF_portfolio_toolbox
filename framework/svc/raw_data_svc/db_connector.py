#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-09 

import os, sys, argparse, logging

import yaml
import pymysql

from functools import wraps

__all__ = ['db_connector']

class DbConnector:
    def __init__(self, ) -> None:
        self._db_info_file = None
        self._db_connection = None

        self.setConfigFile()
        self._setDbInfo()

    def _setDbInfo(self):
        with open(self._db_info_file) as f:
            self._db_info = yaml.load(f)

    def _setDbConnection(self):
        self._db_connection = pymysql.connect(
            host  = self._db_info['host'],
            user = self._db_info['user'],
            password  =self._db_info['password'],
            db = self._db_info['db'],
            port = self._db_info['port'],
            charset = 'GBK'
        )

    ##########################################
    # api
    def setConfigFile(self, db_info_file=os.path.join(os.path.dirname(__file__), 'db_info.yaml')):
        self._db_info_file = db_info_file
        self._setDbInfo()
        self._setDbConnection()

    def getDbConnection(self):
        return self._db_connection

    def getDbInfo(self):
        return self._db_info

    

db_connector = DbConnector()

# test
# print(db_connector.getDbConnection())
# db_connector.setConfigFile('db_info.yaml')
# print(db_connector.getDbConnection())