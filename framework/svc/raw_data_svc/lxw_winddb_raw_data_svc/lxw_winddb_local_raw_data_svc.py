#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-11 

import os, sys, argparse, logging
import warnings

raw_data_svc_path = os.path.dirname(__file__)
if raw_data_svc_path not in sys.path:
    sys.path.append(raw_data_svc_path)

import pandas as pd

svc_path = os.path.join(os.path.dirname(__file__), '../..')
if svc_path not in sys.path:
    sys.path.append(svc_path)

from singleton import Singleton

from yaml_svc.yaml_svc import YamlSvc


class LxwWinddbLocalRawDataSvc(Singleton):
    def __init__(self) -> None:
        if not self._isFirstInit():
            return
        # print('init LxwWinddbLocalRawDataSvc')
        super().__init__()
        self._yaml_svc = YamlSvc()
        self.setLocalDbConfigFile()
        self._tables = {}
        self._nav_tables = {}

    def _setLocalDbConfig(self):
        self._local_db_config = self._yaml_svc.loadYaml(self._local_db_config_file)

    def _setLocalDbPath(self):
        self._local_db_path = os.path.join(raw_data_svc_path, self._local_db_config['local_db_loc'])
        assert os.path.isdir(self._local_db_path), 'local_db_path {} do not exist'.format(self._local_db_path)

    def _loadOneTable(self, table):
        if not table in self._local_db_config['tables']:
            return None
        table_file = os.path.join(self._local_db_path, '{}.h5'.format(table))
        if not os.path.isfile(table_file):
            warnings.warn('{} not found, skip it'.format(table_file))
            return None
        print('loading {} from local_db'.format(table))
        if table in self._local_db_config['nav_tables']:
            columns = self._local_db_config['nav_tables'][table]
            self._tables[table] = LocalNavTable(
                table_file, 
                windcode_column = columns['windcode_column'], 
                date_column = columns['date_column'], 
                nav_column = columns['nav_column']
            )
            self._nav_tables[table] = self._tables[table]
        else:
            self._tables[table] = LocalTable(table_file)
        return True

    ###########################################
    # api
        

    def setLocalDbConfigFile(self, local_db_config_file=os.path.join(os.path.dirname(__file__), 'lxw_winddb_local_db.yaml')):
        self._local_db_config_file = local_db_config_file
        self._setLocalDbConfig()
        self._setLocalDbPath()
        

    def getFullTable(self, table_name, columns=None):
        assert table_name, 'table_name must not be empty'
        if table_name not in self._tables:
            if self._loadOneTable(table_name) is None:
                return None
        tmp = self._tables[table_name].getRawData()
        if columns:
            assert isinstance(columns, (list, tuple)), 'columns must be list or tuple'
            return tmp[columns]
        else:
            return tmp

    def getNav(self, table_name, windcode):
        if table_name not in self._tables:
            if self._loadOneTable(table_name) is None:
                return None
        assert table_name in self._nav_tables, '{} has not save to local'
        return self._nav_tables[table_name].getNav(windcode)    


class LocalTable:
    def __init__(self, table_file) -> None:
        self._table_file = table_file
        self._setTableName()
        self._loadTable()

    def _setTableName(self):
        self._table_name = os.path.basename(self._table_file).split('.')[0]

    def _loadTable(self):
        if os.path.isfile(self._table_file):
            self._raw_data = pd.read_hdf(self._table_file, key='data')
        else:
            raise FileNotFoundError('{} not found'.format(self._table_file))

    def getName(self):
        return self._table_name

    def getRawData(self):
        return self._raw_data

class LocalNavTable(LocalTable):
    def __init__(
        self, 
        table_file, 
        windcode_column = None, 
        date_column = None, 
        nav_column = None) -> None:
        super().__init__(table_file)
        assert windcode_column, 'windecode_column is empty'
        self._windecode_column = windcode_column

        assert date_column, 'date_column is empty'
        self._date_column = date_column

        assert nav_column, 'nav_column is empty'
        self._nav_column = nav_column

    def getNav(self, windcode):
        nav_data = self._raw_data[self._raw_data[self._windecode_column]==windcode].sort_values(by=self._date_column)
        if not nav_data.shape[0]:
            warnings.warn('getNav: {} do not in {}'.format(windcode, self._table_name))
        nav_data.index = nav_data[self._date_column]
        return nav_data[self._nav_column]

# local_raw_data_svc = LocalRawDataSvc()

# # test
# aindexeodprices_table = LocalNavTable(
#     os.path.join(os.path.dirname(__file__), '../local_db/aindexeodprices.h5'), 
#     windecode_column='S_INFO_WINDCODE', 
#     date_column='TRADE_DT', 
#     nav_column='S_DQ_CLOSE',)
# print(aindexeodprices_table.getNav('000003.SH'))

# print(local_raw_data_svc.getFullTable('aindexeodprices'))
# print(local_raw_data_svc.getNav('aindexeodprices', '000003.SH'))


