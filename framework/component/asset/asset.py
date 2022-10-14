#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-09-01 

import os, sys, argparse, logging
import warnings

import pandas as pd

asset_path = os.path.dirname(__file__)
if asset_path not in sys.path:
    sys.path.append(asset_path)

from asset_base import AssetBase

framework_path = os.path.join(asset_path, '../..')
if framework_path not in sys.path:
    sys.path.append(framework_path)

from import_func import getSvc
date_svc = getSvc('DateSvc')

class Asset(AssetBase):
    def __init__(self, name) -> None:
        super().__init__(name) 

        self._raw_nav_data = None 
        self._raw_return = None 
        self._raw_data = None

    def setTransectionRate(self, *args, **kwargs):
        assert not self.getPositionManager() is None
        self.getPositionManager().setTransectionRate(*args, **kwargs)

    def setMarginRatio(self, *args, **kwargs):
        assert not self.getPositionManager() is None
        self.getPositionManager().setMarginRatio(*args, **kwargs)

    def getTransectionRate(self):
        assert not self.getPositionManager() is None
        self.getPositionManager()._transection_rate

    def print(self, level=0):
        print('{}asset: {}'.format('\t'*level, self._name))

    def setRawNavData(self, raw_nav_data):
        self._raw_nav_data = date_svc.formatIndex(raw_nav_data)
        self._raw_return = self._raw_nav_data / self._raw_nav_data.shift() - 1
        self._raw_return.fillna(0, inplace=True)
        self._raw_data = self._raw_nav_data

    def setRawData(self, raw_data, nav_column=None):
        '''
        extend setRawNavData
        '''
        self._raw_data = date_svc.formatIndex(raw_data)
        if isinstance(self._raw_data, pd.Series):
            self._raw_nav_data = self._raw_data
        else:
            self._raw_nav_data = self._raw_data[nav_column]
        self._raw_return = self._raw_nav_data / self._raw_nav_data.shift() - 1
        self._raw_return.fillna(0, inplace=True)

    def getRawNavData(self):
        return self._raw_nav_data

    def setIdDate(self, id_date, *args):
        super().setIdDate(id_date)
        if args and not self._raw_data is None:
            self._setUsableNavData(id_date, *args)

    def getIdDate(self):
        return self._id_date

    def _setUsableNavData(self, *args):
        self._usable_raw_data = date_svc.cutData(self._raw_data, *args)
        self._usable_nav_data = date_svc.cutData(self._raw_nav_data, *args)
        self._usable_return_data = date_svc.cutData(self._raw_return, *args)

    def getUsableRawData(self):
        return self._usable_raw_data

    def getUsableNavData(self):
        return self._usable_nav_data

    def getUsableReturnData(self):
        return self._usable_return_data

    def isTradable(self, id_date):
        return self._raw_nav_data.index[0] <= pd.Timestamp(id_date) <= self._raw_nav_data.index[-1]

    def isDelisted(self, id_date):
        return pd.Timestamp(id_date) > self._raw_nav_data.index[-1]

    def getAge(self, id_date, type_='trade'):
        if not self.isTradable(id_date):
            return -1
        if type_ == 'raw':
            return (pd.Timestamp(id_date) - self._raw_nav_data.index[0]).days
        elif type_ == 'trade':
            return self._raw_data.loc[: id_date].shape[0]

    def executeOrder(self, order):
        assert not self.getPositionManager() is None
        if self.isTradable(order.date):
            return self.getPositionManager().executeOrder(order)
        return 0

    def updateAfterClose(self):
        assert not self.getPositionManager() is None
        if self.isTradable(self._id_date):
            self.getPositionManager().updateAfterClose(self._raw_nav_data.loc[self._id_date])

    def updateAfterExecuteOrders(self):
        assert not self.getPositionManager() is None
        self.getPositionManager().updateAfterExecuteOrders()

    

# # test
