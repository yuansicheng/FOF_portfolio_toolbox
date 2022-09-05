#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-11 

import os, sys, argparse, logging

raw_data_svc_path = os.path.dirname(__file__)
if raw_data_svc_path not in sys.path:
    sys.path.append(raw_data_svc_path)

svc_path = os.path.join(raw_data_svc_path, '..')
if svc_path not in sys.path:
    sys.path.append(svc_path)

from singleton import Singleton

from sql_raw_data_svc import SqlRawDataSvc
from local_raw_data_svc import LocalRawDataSvc

# __all__ = ['raw_data_svc']

class RawDataSvc(Singleton):
    def __init__(self) -> None:
        if not self._isFirstInit():
            return
        print('init RawDataSvc')
        self._sql_raw_data_svc = SqlRawDataSvc()
        self._local_raw_data_svc = LocalRawDataSvc()

    ###########################################
    # api
    def setDbConfigFile(self, db_info_file):
        self._sql_raw_data_svc._db_connector.setConfigFile(db_info_file=db_info_file)

    def setTableColumnPath(self, table_column_path):
        self._sql_raw_data_svc._table_column_svc.setConfigFile(table_column_path=table_column_path)

    def setLocalDbConfigFile(self, local_db_config_file):
        self._local_raw_data_svc.setLocalDbConfigFile(local_db_config_file=local_db_config_file)

    def sqlQuery(self, sql):
        print('raw_data_svc.sqlQuery: {}'.format(sql))
        return self._sql_raw_data_svc.query(sql)

    def getFullTable(self, table_name, columns=None):
        # try local first, then query sql
        tmp = self._local_raw_data_svc.getFullTable(table_name, columns=columns)
        if not tmp is None:
            return tmp
        return self._sql_raw_data_svc.getFullTable(table_name, columns=columns)

    def getNav(self, table_name, windcode):
        return self._local_raw_data_svc.getNav(table_name, windcode)

    def getTradeDays(self, mode='SSE'):
        sql = "SELECT TRADE_DAYS FROM asharecalendar WHERE S_INFO_EXCHMARKET='{}' ORDER BY TRADE_DAYS".format(mode)
        return self.sqlQuery(sql)['TRADE_DAYS']

# raw_data_svc = RawDataSvc()


# # test
# print(raw_data_svc.getNav('aindexeodprices', '000003.SH'))
# print(raw_data_svc.getFullTable('aindexeodprices'))
# print(raw_data_svc.sqlQuery("SELECT * from information_schema.TABLES WHERE TABLE_SCHEMA='winddb_alicloud'"))
# print(raw_data_svc.getFullTable('asharecalendar', columns=['TRADE_DAYS']))