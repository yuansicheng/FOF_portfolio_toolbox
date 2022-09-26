#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-09 

import os, sys, argparse, logging

import yaml
import pymysql
from sqlalchemy import create_engine

db_connector_svc_path = os.path.join(os.path.dirname(__file__), '..')
if db_connector_svc_path not in sys.path:
    sys.path.append(db_connector_svc_path)

from db_connector_svc_base import DbConnectorSvcBase

class MysqlDbConnectorSvc(DbConnectorSvcBase):
    def __init__(self, ) -> None:
        super().__init__()
        print('init MysqlDbConnectorSvc')

    def _createDbConnection(self, db_info):
        DB_URI = 'mysql+pymysql://{username}:{pwd}@{host}:{port}/{db}?charset=utf8'.format(
            username = db_info['user'], 
            pwd = db_info['password'], 
            host = db_info['host'], 
            port = db_info['port'], 
            db = db_info['db'])
        return create_engine(DB_URI)
