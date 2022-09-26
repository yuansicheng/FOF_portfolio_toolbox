#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-09-09 

import os, sys, argparse, logging

import pandas as pd
import warnings

component_path = os.path.join(os.path.dirname(__file__), '..')
if component_path not in sys.path:
    sys.path.append(component_path)

from historical_data_manager.historical_data_manager import HistoricalDataManager

class PositionManagerBase:
    def __init__(self) -> None:
        self._historical_data_manager = HistoricalDataManager()
        self._id_date = None

        self._columns = [ 
            'position', # 仓位，持有资产的总价值           
            'weight', # 权重
            'transection_cost', # 总交易成本
            'investment', # 投资
            'hodlding_return', # 持有收益 = 仓位-总投资
            'hodlding_yield', # 持有收益率 = 持有收益/总投资
            'historical_return', # 历史收益，执行卖出操作后累加
            'total_return', # 总收益 = 持有收益 + 历史收益 - 交易成本
            ]
        for column in self._columns:
            self.addPositionData(column, 0)
        
    def addPositionData(self, name, init_value=0):
        setattr(self, name, init_value)
        self._historical_data_manager.addColumn(name)

    def getHistoricalData(self):
        return self._historical_data_manager.getData()

    def getData(self, id_date=None, key=None):
        return self._historical_data_manager.getData(index=id_date, column=key)

    def getIdDate(self):
        return self._id_date

    def setIdDate(self, id_date):
        self._id_date = id_date

    def updateHistoricalData(self):
        self._historical_data_manager.addData([getattr(self, name) for name in self._columns], index=self._id_date)

    def updateAfterClose(self, *args, **kwargs):
        raise NotImplementedError

    def updateAfterExecuteOrders(self, *args, **kwargs):
        raise NotImplementedError

    def updateWeight(self, total):
        self.weight = self.position / total if total != 0 else 0

    def updateReturns(self):
        self.holding_return = self.position - self.investment
        self.holding_yield = self.holding_return / self.investment if self.investment else 0
        self.total_return = self.holding_return + self.historical_return - self.transection_cost


# test
# pmb = PositionManagerBase()
# print(pmb.getHistoricalData())
    
        