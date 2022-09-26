#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-29 

import os, sys, argparse, logging

from copy import deepcopy

class AssetBase:
    def __init__(self, name) -> None:
        assert name, 'name must not be None'
        self._name = name

        self._position_manager = None

        self.setWeightRange()

    def getPositionManager(self):
        return self._position_manager

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
