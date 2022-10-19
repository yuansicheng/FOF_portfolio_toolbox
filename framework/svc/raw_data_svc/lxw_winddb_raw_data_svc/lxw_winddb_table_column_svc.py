#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-11 

import os, sys, argparse, logging

import yaml

svc_path = os.path.join(os.path.dirname(__file__), '..')
if svc_path not in sys.path:
    sys.path.append(svc_path)

from singleton import Singleton
from importlib import import_module
yaml_svc = getattr(import_module('yaml_svc.yaml_svc'), 'YamlSvc')()

class LxwWinddbTableColumnSvc(Singleton):
    def __init__(self) -> None:
        if not self._isFirstInit():
            return
        # print('init TableColumnSvc')
        self._table_column_path = None
        self.setConfigFile()

    def _setTableColumnDict(self):
        self._table_column_dict = {}
        for table_column_file in os.listdir(self._table_column_path):
            self._table_column_dict[self._file2Table(table_column_file)] = yaml_svc.loadYaml(os.path.join(self._table_column_path, table_column_file))


    def _file2Table(self, file_name):
        return file_name.split('.')[0]

    ##########################################################
    # api
    def setConfigFile(self, table_column_path=os.path.join(os.path.dirname(__file__), 'table_columns')):
        self._table_column_path = table_column_path
        self._setTableColumnDict()

    def getTableColumn(self, table_name):
        table_name = table_name.lower()
        if table_name in self._table_column_dict:
            return self._table_column_dict[table_name]
        else:
            return ['*']

# table_column_svc = TableColumnSvc()

# test
# print(table_column_svc.getTableColumn('chinamutualfunddescription'))

