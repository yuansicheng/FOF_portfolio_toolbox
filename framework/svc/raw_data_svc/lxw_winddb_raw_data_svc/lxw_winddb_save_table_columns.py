#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-11 

from genericpath import isfile
import os, sys, argparse, logging

from tqdm import tqdm

this_path = os.path.dirname(__file__)
if this_path not in sys.path:
    sys.path.append(this_path)

from lxw_winddb_sql_raw_data_svc import LxwWinddbSqlRawDataSvc

class SaveTableColumns:
    def __init__(self, table_column_path = os.path.join(this_path, 'table_columns')) -> None:
        self._table_column_path = table_column_path
        if not os.path.isdir(self._table_column_path):
            os.makedirs(self._table_column_path)
        self._raw_data_svc = LxwWinddbSqlRawDataSvc()

        self._db_name = 'winddb_alicloud'

    def _setTables(self):
        sql = "SELECT TABLE_NAME from information_schema.TABLES WHERE TABLE_SCHEMA='{}'".format(self._db_name)
        self._tables = self._raw_data_svc.query(sql)['TABLE_NAME']

    def _getTableColumns(self, table_name):
        sql = "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_name='{}'".format(table_name)
        return list(self._raw_data_svc.query(sql)['COLUMN_NAME'])

    def _saveTableColumns(self):
        for i in tqdm(
            range(len(self._tables)), 
            desc='save table columns', 
            unit='table'
        ):
            self._saveOne(self._tables[i])

    def _saveOne(self, table_name):
        table_column_file = os.path.join(self._table_column_path, '{}.yaml'.format(table_name))
        if os.path.isfile(table_column_file):
            return
        columns = self._getTableColumns(table_name)
        with open(table_column_file, 'w') as f:
            f.write('\n'.join(['- '+c for c in columns]))

    ########################################
    # api
    def saveAll(self):
        self._setTables()
        self._saveTableColumns()

    


save_table_columns = SaveTableColumns()
save_table_columns.saveAll()

