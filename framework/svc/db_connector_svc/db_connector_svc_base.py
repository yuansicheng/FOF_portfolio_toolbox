#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-09 

import os, sys, argparse, logging

svc_path = os.path.join(os.path.dirname(__file__), '..')
if svc_path not in sys.path:
    sys.path.append(svc_path)

from singleton import Singleton
from importlib import import_module
yaml_svc = getattr(import_module('yaml_svc.yaml_svc'), 'YamlSvc')()

class DbConnectorSvcBase(Singleton):
    def __init__(self, ) -> None:
        if not self._isFirstInit():
            return
        super().__init__()
        # print('init DbConnectorSvc')

        self._db_connection = {}

    def _createDbConnection(self, db_info):
        raise NotImplementedError

    ##########################################
    # api
    def addDbConnection(self, name, db_info_file):
        db_info = yaml_svc.loadYaml(db_info_file)
        self._db_connection[name] = self._createDbConnection(db_info)

    def getDbConnection(self, name):
        return self._db_connection[name]

