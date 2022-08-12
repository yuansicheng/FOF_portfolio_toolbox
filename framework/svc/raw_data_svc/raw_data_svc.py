#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-11 

import os, sys, argparse, logging

raw_data_svc_path = os.path.dirname(__file__)
if raw_data_svc_path not in sys.path:
    sys.path.append(raw_data_svc_path)

from sql_raw_data_svc import sql_raw_data_svc
from local_raw_data_svc import local_raw_data_svc

__all__ = ['raw_data_svc']

class RawDataSvc:
    def __init__(self) -> None:
        print('init raw_data_svc')
        self._sql_raw_data_svc = sql_raw_data_svc
        self._local_raw_data_svc = local_raw_data_svc

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

raw_data_svc = RawDataSvc()

# # test
# print(raw_data_svc.getNav('aindexeodprices', '000003.SH'))
# print(raw_data_svc.getFullTable('aindexeodprices'))
# print(raw_data_svc.sqlQuery("SELECT * from information_schema.TABLES WHERE TABLE_SCHEMA='winddb_alicloud'"))
# print(raw_data_svc.getFullTable('asharecalendar', columns=['TRADE_DAYS']))