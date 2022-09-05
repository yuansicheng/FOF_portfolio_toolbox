#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-29 

import os, sys, argparse, logging

framework_path = os.path.join(os.path.dirname(__file__), '../..')
if framework_path not in sys.path:
    sys.path.append(framework_path)

from import_func import getSvc
indicator_svc = getSvc('IndicatorSvc')

class AssetBase:
    def __init__(self, name) -> None:
        assert name, 'name must not be None'
        self._name = name

        self._setIndicatorFuns()

        self._child_group = []
        self._child_asset = []   

        self._weight_range = [0, 1] 

    def _setIndicatorFuns(self):
        for func in [func for func in dir(indicator_svc) if func.startswith('get')]:
            setattr(self, func, getattr(indicator_svc, func))

    def print(self, level=0):
        raise NotImplementedError

    def getChildGroup(self):
        raise NotImplementedError 

    def getChildAsset(self):
        raise NotImplementedError 

    def addChildGroup(self):
        raise NotImplementedError 

    def addChildAsset(self):
        raise NotImplementedError 

    def getName(self):
        return self._name

    def getWeightRange(self):
        return self._weight_range


# # test
# a1 = AssetBase(1)
# a2 = AssetBase(2)
