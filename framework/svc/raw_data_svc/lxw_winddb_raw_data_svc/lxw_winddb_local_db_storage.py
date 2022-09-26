#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-10 

import os, sys, argparse, logging

from datetime import datetime
import pandas as pd
from tqdm import tqdm

raw_data_svc_path = os.path.dirname(__file__)
if raw_data_svc_path not in sys.path:
    sys.path.append(raw_data_svc_path)

svc_path = os.path.join(os.path.dirname(__file__), '../..')
if svc_path not in sys.path:
    sys.path.append(svc_path)

from lxw_winddb_sql_raw_data_svc import LxwWinddbSqlRawDataSvc as RawDataSvc
from lxw_winddb_table_column_svc import LxwWinddbTableColumnSvc as TableColumnSvc

from yaml_svc.yaml_svc import YamlSvc

class LxwWinddbLocalDbStorage:
    def __init__(self, local_db_file=os.path.join(os.path.dirname(__file__), 'lxw_winddb_local_db.yaml')) -> None:
        self._local_db_file = local_db_file
        self._raw_data_svc = RawDataSvc()
        self._table_column_svc = TableColumnSvc()
        self._yaml_svc = YamlSvc()
        self._setLocalDbInfo()
        self._setDate()
        self._checkLocalDbPath()

        # print(self._local_db_info)

    def _setLocalDbInfo(self):
        self._local_db_info = self._yaml_svc.loadYaml(self._local_db_file)
        self._tables = self._local_db_info['tables']
        self._nav_tables = self._local_db_info['nav_tables']

    def _checkLocalDbPath(self):
        self._local_db_path = os.path.join(raw_data_svc_path, self._local_db_info['local_db_loc'])
        if not os.path.isdir(self._local_db_path):
            os.makedirs(self._local_db_path)
        print('self._local_db_path: ', os.path.abspath(self._local_db_path))

    def _setDate(self):
        # same format as mysql
        self._date = datetime.now().strftime('%Y-%m-%d')
        self._date_series = pd.Series([self._date])

    def _saveLocalFile(self):
        for table in tqdm(
            self._tables, 
            desc='save file', 
            unit='file'):
            self._saveOneTable(table)

        # for nav_table in tqdm(
        #     self._nav_tables, 
        #     desc='save nav file', 
        #     unit='file'):
        #     self._divideAsset(table)

    def _saveOneTable(self, table):
        table_file = os.path.join(self._local_db_path, '{}.h5'.format(table))
        columns = self._table_column_svc.getTableColumn(table)

        NEW_COLUMN_FLAG = False

        # case 1: file exists and not add new columns, update data after last_update_date
        if os.path.isfile(table_file):
            last_update_date = pd.read_hdf(table_file, key='last_update_date').values[0]
            old_data = pd.read_hdf(table_file, key='data')
            old_columns = old_data.columns

            diff_columns = list(set(columns) - set(old_columns))

            if diff_columns:
                NEW_COLUMN_FLAG = True
                os.remove(table_file)
            else:
                sql = "SELECT {} FROM {} WHERE OPDATE>='{}'".format(','.join(columns), table, last_update_date)
                new_data = self._raw_data_svc.query(sql)
                data = pd.concat([old_data, new_data]).drop_duplicates()

        # case 2: file not exists or add new columns
        if not os.path.isfile(table_file) or NEW_COLUMN_FLAG:
            data = self._raw_data_svc.getFullTable(table, columns=columns)
        
        # save data, use the best compress method
        data.to_hdf(table_file, key='data', encoding='utf-8', complevel=9, complib='blosc', format='table')
        # update last_update_date
        self._date_series.to_hdf(table_file, key='last_update_date')

    # we do not use this function because groupby operation cost to much time
    def _divideAsset(self, table):
        table_file = os.path.join(self._local_db_path, '{}.h5'.format(table))
        table_info = self._local_db_info['nav_tables'][table]
        # print(os.path.abspath(table_file))
        assert os.path.isfile(table_file)
        tabel_divide_file = os.path.join(self._local_db_path, '{}_divide.h5'.format(table))

        data = pd.read_hdf(table_file, 'data')
        data_groupby = data.groupby(by=table_info['windcode_column'])
        for windcode, group_data in tqdm(data_groupby):
            group_data.drop(windcode, axis=1, inplace=True)
            group_data.to_hdf(tabel_divide_file, key=windcode, encoding='utf-8', complevel=9, complib='blosc', format='table')
        




    #######################################
    # api
    def save(self):
        self._saveLocalFile()



local_db_storage = LxwWinddbLocalDbStorage()
local_db_storage.save()


# test
# local_db_loc = 'local_db'
# data = pd.read_hdf(os.path.join(local_db_loc, 'aindexeodprices.h5'), key='last_update_date')
# print(data)