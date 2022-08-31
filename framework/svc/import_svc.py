#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-17 

import os, sys, argparse, logging

svc_path = os.path.dirname(__file__)
if svc_path not in sys.path:
    sys.path.append(svc_path)

from singleton import Singleton
import yaml
from importlib import import_module
yaml_svc = getattr(import_module('yaml_svc.yaml_svc'), 'YamlSvc')()

__all__ = ['getSvc']

class ImportSvc(Singleton):
    def __init__(self) -> None:
        if not self._isFirstInit():
            return
        self.setConfigFile()

    def _setSvcInfo(self):
        self._svc_info = yaml_svc.loadYaml(self._svc_file)

    def setConfigFile(self, svc_file=os.path.join(svc_path, 'svc.yaml')):
        self._svc_file = svc_file
        self._setSvcInfo()

    def getSvc(self, svc_name):
        assert svc_name in self._svc_info, 'svc {} has not registered'.format(svc_name)
        path = self._svc_info[svc_name].replace('/', '.').replace('.py', '')
        module = import_module(path)
        return getattr(module, svc_name)()
        
        
        

import_svc = ImportSvc()

def getSvc(svc_name):
    # return an object of target svc
    return import_svc.getSvc(svc_name)

# test
# raw_data_svc = getSvc('RawDataSvc')
