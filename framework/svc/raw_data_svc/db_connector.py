#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-09 

import os, sys, argparse, logging

import yaml
import pymysql
from sqlalchemy import create_engine

svc_path = os.path.join(os.path.dirname(__file__), '..')
if svc_path not in sys.path:
    sys.path.append(svc_path)

from singleton import Singleton
from importlib import import_module
yaml_svc = getattr(import_module('yaml_svc.yaml_svc'), 'YamlSvc')()

class DbConnector(Singleton):
    def __init__(self, ) -> None:
        if not self._isFirstInit():
            return
        print('init DbConnector')
        self.setConfigFile()

    def _setDbInfo(self):
        self._db_info = yaml_svc.loadYaml(self._db_info_file)

    def _setDbConnection(self):
        self._db_connection = pymysql.connect(
            host  = self._db_info['host'],
            user = self._db_info['user'],
            password = self._db_info['password'],
            db = self._db_info['db'],
            port = self._db_info['port'],
            charset = 'GBK'
        )

    # better way for py38
    def _setDbConnectionAlchemy(self):
        DB_URI = 'mysql+pymysql://{username}:{pwd}@{host}:{port}/{db}?charset=utf8'.format(
            username = self._db_info['user'], 
            pwd = self._db_info['password'], 
            host = self._db_info['host'], 
            port = self._db_info['port'], 
            db = self._db_info['db'])
        self._db_connection = create_engine(DB_URI)

    ##########################################
    # api
    def setConfigFile(self, db_info_file=os.path.join(os.path.dirname(__file__), 'db_info.yaml')):
        self._db_info_file = db_info_file
        self._setDbInfo()
        self._setDbConnectionAlchemy()

    def getDbConnection(self):
        return self._db_connection

    def getDbInfo(self):
        return self._db_info


# test
# print(db_connector.getDbConnection())
# db_connector.setConfigFile('db_info.yaml')
# print(db_connector.getDbConnection())