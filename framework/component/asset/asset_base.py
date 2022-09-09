#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-29 

import os, sys, argparse, logging

from copy import deepcopy

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
        self.setWeightRange()
        
    def _setIndicatorFuns(self):
        for func in [func for func in dir(indicator_svc) if func.startswith('get')]:
            setattr(self, func, getattr(indicator_svc, func))

    def print(self, level=0):
        raise NotImplementedError

    def getName(self):
        return self._name

    def setWeightRange(self, weight_range=[0, 1]):
        assert isinstance(weight_range, (list, tuple)) and len(weight_range) == 2
        self._weight_range = weight_range

    def getWeightRange(self):
        return self._weight_range

    def copy(self):
        return deepcopy(self)


# # test
# a1 = AssetBase(1)
# a2 = AssetBase(2)
