#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-09 

import os, sys, argparse, logging

svc_path = os.path.join(os.path.dirname(__file__), '../..')
if svc_path not in sys.path:
    sys.path.append(svc_path)

this_path = os.path.dirname(__file__)
if this_path not in sys.path:
    sys.path.append(this_path)

from db_connector_svc.mysql_db_connector_svc.mysql_db_connector_svc import MysqlDbConnectorSvc
from lxw_winddb_table_column_svc import LxwWinddbTableColumnSvc

from singleton import Singleton

import pandas as pd
from tqdm import tqdm

class LxwWinddbSqlRawDataSvc(Singleton):
    def __init__(self) -> None:
        if not self._isFirstInit():
            return
        # print('init LxwWinddbSqlRawDataSvc')
        super().__init__()
        self._db_connector = MysqlDbConnectorSvc()
        self._table_column_svc = LxwWinddbTableColumnSvc()

        self.setConfigFile()


    def _getFullTableByYear(self, table_name, columns):
        data_by_year = []
        years = self._getTableDistinctYears(table_name)
        for i in tqdm(
            range(len(years)), 
            desc='fetching {}'.format(table_name), 
            unit='year'
        ):
            sql = 'SELECT {} FROM {} WHERE YEAR(OPDATE)={}'.format(columns, table_name, years[i])
            data_by_year.append(self.query(sql=sql))
        return pd.concat(data_by_year)

    def _getTableDistinctYears(self, table_name):
        # for get data by year
        sql = 'SELECT DISTINCT YEAR(OPDATE) AS year from {}'.format(table_name)
        return self.query(sql)['year']

    def _getTableRowNum(self, table_name):
        # total lins of the table
        sql = "SELECT TABLE_ROWS FROM information_schema.TABLES WHERE TABLE_NAME='{}'".format(table_name)
        return self.query(sql)['TABLE_ROWS'][0]

    ###########################################
    # api
    def setConfigFile(self, db_info_file=os.path.join(this_path, 'lxw_winddb_info.yaml')):
        self._db_connector.addDbConnection('lxw_winddb', db_info_file)
        self._db_connection = self._db_connector.getDbConnection('lxw_winddb')

    def query(self, sql):
        assert sql, 'sql must not be empty'
        print('raw_data_svc.sqlQuery: {}'.format(sql))
        return pd.read_sql(sql, self._db_connection)

    def getFullTable(self, table_name, columns=None):
        assert table_name, 'table_name must not be empty'
        if columns:
            assert isinstance(columns, (list, tuple)), 'columns must be list or tuple'
        row_num = self._getTableRowNum(table_name)
        if not columns:
            columns = self._table_column_svc.getTableColumn(table_name)
        columns = ','.join(columns)

        if row_num < 100000:
            sql = 'SELECT {} from {}'.format(columns, table_name)
            return self.query(sql=sql)
        else:
            return self._getFullTableByYear(table_name, columns)
        



# # test
# sql_raw_data_svc = LxwWinddbSqlRawDataSvc()
# print(sql_raw_data_svc.getFullTable('chinamutualfunddescription', columns=['OPDATE']))
