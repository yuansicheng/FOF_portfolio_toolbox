#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-09-01 

import os, sys, argparse, logging

import pandas as pd

asset_path = os.path.dirname(__file__)
if asset_path not in sys.path:
    sys.path.append(asset_path)

from asset_base import AssetBase

framework_path = os.path.join(asset_path, '../..')
if framework_path not in sys.path:
    sys.path.append(framework_path)

from import_func import getSvc
raw_data_svc = getSvc('RawDataSvc')
date_svc = getSvc('DateSvc')

class Asset(AssetBase):
    def __init__(self, name) -> None:
        super().__init__(name)   

    def print(self, level=0):
        print('{}asset: {}'.format('\t'*level, self._name))

    def setRawNavdata(self, raw_nav_data):
        self._raw_nav_data = date_svc.formatIndex(raw_nav_data)

    def getRawNavData(self):
        return self._raw_nav_data

    def _setRawNavDataFromRawDataSvc(self, table_name):
        self.setRawNavdata(raw_data_svc.getNav(table_name, self._windcode))

    def setIdDate(self, id_date, *args):
        self._id_date = id_date
        self.setUsableNavData(id_date, *args)

    def getIdDate(self):
        return self._id_date

    def setUsableNavData(self, *args):
        self.usable_nav_data = date_svc.cutData(self._raw_nav_data, *args)

    def getUsableNavData(self):
        return self.usable_nav_data

class WindAsset(Asset):
    def __init__(self, name, windcode) -> None:
        super().__init__(name)
        self._windcode = windcode

    def getWindcode(self):
        return self._windcode


class IndexAsset(WindAsset):
    def __init__(self, name, windcode) -> None:
        super().__init__(name, windcode)       
        self._setRawNavDataFromRawDataSvc('aindexeodprices')
        

class StockAsset(WindAsset):
    def __init__(self, name, windcode) -> None:
        super().__init__(name, windcode)
        self._setRawNavDataFromRawDataSvc('ashareeodprices')

class FundAsset(WindAsset):
    def __init__(self, name, windcode) -> None:
        super().__init__(name, windcode)
        self._setRawNavDataFromRawDataSvc('chinamutualfundnav')

    

# # test
# from datetime import date
# a = IndexAsset('1', '000003.SH')
# a.setIdDate(date(2020, 12, 31), 22)
# print(a.usable_nav_data, a.getSharpe(a.usable_nav_data))