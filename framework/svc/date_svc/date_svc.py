#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-12 

from datetime import datetime
import os, sys, argparse, logging

import pandas as pd
import warnings

framework_path = os.path.join(os.path.dirname(__file__), '../..')
if framework_path not in sys.path:
    sys.path.append(framework_path)

from import_func import getSvc
raw_data_svc = getSvc('RawDataSvc')

from singleton import Singleton

class DateSvc(Singleton):
    def __init__(self) -> None:
        if not self._isFirstInit():
            return
        print('init DateSvc')
        self.setMode()

    def _setTradeDays(self):
        self._trade_days = raw_data_svc.getTradeDays(mode=self._mode)
        self._trade_days = pd.to_datetime(self._trade_days)
        self._trade_days.index = self._trade_days.values

    ###########################################
    # api

    def setMode(self, mode='SSE'):
        self._mode = mode
        self._setTradeDays()

    def formatIndex(self, data):
        data.index = pd.to_datetime(data.index)
        return data

    def getAllTradeDays(self):
        return self._trade_days

    def cutDataWithIndex(self, data, index):
        assert not [i for i in index if i not in self.getAllTradeDays()], 'index must in all_trade_days'
        found_index = [i for i in index if i in data.index]
        not_found_index =  [i for i in index if i not in data.index]
        if not_found_index:
            warnings.warn('DateSvc.cutDataWithIndex: index {} not found in data.index'.format(not_found_index))
        if isinstance(data, pd.Series):
            tmp = pd.Series(index=index, dtype=float)
        else:
            tmp = pd.DataFrame(index=index, columns=data.columns)
        tmp.loc[found_index] = data.loc[found_index]
        return tmp


    def cutDataWithWindow(self, data, id_date, window):
        return self.cutDataWithIndex(data, self.getIndexWithWindow(id_date, window))


    def cutDataWithRange(self, data, start_date, end_date):
        return self.cutDataWithIndex(data, self.getIndexWithRange(start_date, end_date))

    def getIndexWithWindow(self, id_date, window):
        assert self.getAllTradeDays()[0].date() < id_date < self.getAllTradeDays()[-1].date(), 'id_date {} out of range'.format(id_date)
        index = self.getAllTradeDays().loc[:id_date]
        assert index.shape[0] >= window, 'do not have enough date for window'
        return index.iloc[-window:]

    def getIndexWithRange(self, start_date, end_date):
        assert self.getAllTradeDays()[0].date() <= start_date <= end_date <= self.getAllTradeDays()[-1].date(), 'start_date {} or end_date {} out of range'.format(start_date, end_date)
        return self.getAllTradeDays().loc[start_date:end_date]

    def getIndex(self, *args):
        if not len(args)==2:
            return None
        if isinstance(args[1], int):
            return self.getIndexWithWindow(*args)
        else:
            return self.getIndexWithRange(*args)

    def cutData(self, data, *args):
        if not args:
            return None
        if len(args) == 1:
            return self.cutDataWithIndex(data, *args)
        elif len(args) == 2:
            return self.cutDataWithIndex(data, self.getIndex(*args))




# # test
# date_svc = DateSvc()
# print(date_svc.getIndex(datetime(2020,1,1),datetime(2020,1,31)))



