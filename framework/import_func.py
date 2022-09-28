#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-17 

import os, sys, argparse, logging

framework_path = os.path.dirname(__file__)
if framework_path not in sys.path:
    sys.path.append(framework_path)

from svc.singleton import Singleton
from importlib import import_module
yaml_svc = getattr(import_module('svc.yaml_svc.yaml_svc'), 'YamlSvc')()

__all__ = ['getSvc']

class ImportObj(Singleton):
    def __init__(self) -> None:
        if not self._isFirstInit():
            return
        self.setConfigFile()

    def _setInfo(self):
        self._info = yaml_svc.loadYaml(self._info_file)

    def setConfigFile(self, info_file=os.path.join(framework_path, 'framework.yaml')):
        self._info_file = info_file
        self._setInfo()

    def getObj(self, type_, name):
        assert type_ in self._info and name in self._info[type_]
        path = (type_ + '.' + self._info[type_][name]).replace('/', '.').replace('.py', '')
        module = import_module(path)
        return getattr(module, name)()
        
        
        

import_obj = ImportObj()

def getSvc(svc_name):
    # return an object of target svc
    return import_obj.getObj('svc', svc_name)


