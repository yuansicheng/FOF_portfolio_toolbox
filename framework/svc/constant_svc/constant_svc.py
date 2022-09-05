#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-18 

import os, sys, argparse, logging

svc_path = os.path.join(os.path.dirname(__file__), '..')
if svc_path not in sys.path:
    sys.path.append(svc_path)

from singleton import Singleton

from importlib import import_module
yaml_svc = getattr(import_module('yaml_svc.yaml_svc'), 'YamlSvc')()

class ConstantSvc(Singleton):
    def __init__(self, ) -> None:
        if not self._isFirstInit():
            return
        print('init ConstantSvc')
        self.setConfigFile()

    def _setConstantInfo(self):
        self._constant = yaml_svc.loadYaml(self._constant_file)
        for k, v in self._constant.items():
            setattr(self, k , v)

    ##########################################
    # api
    def setConfigFile(self, constant_file=os.path.join(os.path.dirname(__file__), 'constant.yaml')):
        self._constant_file = constant_file
        self._setConstantInfo()

    def getConstant(self, constant_name):
        assert constant_name in self._constant, 'constant {} not found'
        return self._constant[constant_name]

# test
# cons_svc = ConstantSvc()
# print(cons_svc.DAY_OF_YEAR)
# print(cons_svc.getConstant('RISK_FREE'))