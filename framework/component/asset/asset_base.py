#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-29 

import os, sys, argparse, logging

from copy import deepcopy

class AssetBase:
    def __init__(self, name) -> None:
        assert not name is None, 'name must not be None'
        self._name = name

        self._id_date = None

        self._position_manager = None
        self.setWeightRange()

    def setIdDate(self, id_date):
        self._id_date = id_date
        if self.getPositionManager():
            self.getPositionManager().setIdDate(id_date)

    def setPositionManager(self, position_manager):
        self._position_manager = position_manager

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

    def updateHistoricalData(self):
        self.getPositionManager().updateHistoricalData()

    def updateAfterClose(self, *args, **kwargs):
        raise NotImplementedError

    def updateAfterExecuteOrders(self, *args, **kwargs):
        raise NotImplementedError

    def updateWeight(self, total, truth_total):
        return self.getPositionManager().updateWeight(total, truth_total)

    


# # test
# a1 = AssetBase(1)
# a2 = AssetBase(2)
