#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-12 

from datetime import datetime, date
import os, sys, argparse, logging

import pandas as pd
import warnings

svc_path = os.path.join(os.path.dirname(__file__), '..')
if svc_path not in sys.path:
    sys.path.append(svc_path)

from singleton import Singleton

class DateSvc(Singleton):
    def __init__(self) -> None:
        if not self._isFirstInit():
            return
        print('init DateSvc')
        self._trade_days = None

    ###########################################
    # api

    def setTradeDays(self, trade_days):
        self._trade_days = trade_days
        self._trade_days = pd.to_datetime(self._trade_days)
        self._trade_days.index = self._trade_days.values

    def formatIndex(self, data):
        data.index = pd.to_datetime(data.index)
        return data

    def getAllTradeDays(self):
        assert not self._trade_days is None, 'Please setTradeDays first'
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
        assert self.getAllTradeDays()[0] < pd.to_datetime(id_date) < self.getAllTradeDays()[-1], 'id_date {} out of range'.format(id_date)
        # drop id_date
        index = self.getAllTradeDays().loc[:id_date].iloc[:-1]
        assert index.shape[0] >= window, 'do not have enough date for window'
        return index.iloc[-window:]

    def getIndexWithRange(self, start_date, end_date):
        assert self.getAllTradeDays()[0] <= pd.to_datetime(start_date) <= pd.to_datetime(end_date) <= self.getAllTradeDays()[-1], 'start_date {} or end_date {} out of range'.format(start_date, end_date)
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

    def filterDateIndex(self, date_index, frequency=1):
        assert isinstance(frequency, int) or frequency in ['weekly', 'monthly', 'quarterly']

        # case 1: int
        if isinstance(frequency, int):
            return [date_index[i] for i in range(len(date_index)) if i % frequency==0]

        # case 2: weekly, monthly or quarterly
        tmp = pd.DataFrame()
        tmp['date'] = date_index
        tmp['year'] = [d.year for d in date_index]
        if frequency == 'weekly':
            tmp['week_of_year'] = [d.weekofyear for d in date_index]
            return list(tmp.groupby(['year', 'week_of_year']).first()['date'])
        if frequency == 'monthly':
            tmp['month'] = [d.month for d in date_index]
            return list(tmp.groupby(['year', 'month']).first()['date'])
        if frequency == 'quarterly':
            tmp['quarter'] = [(d.month-1)//3 for d in date_index]
            return list(tmp.groupby(['year', 'quarter']).first()['date'].values)





# # test
# from raw_data_svc.lxw_winddb_raw_data_svc.lxw_winddb_raw_data_svc import LxwWinddbRawDataSvc as RawDataSvc
# raw_data_svc = RawDataSvc()
# date_svc = DateSvc()
# date_svc.setTradeDays(raw_data_svc.getTradeDays())
# index = date_svc.getIndex(datetime(2020,1,1),datetime(2020,12,31))

# print(date_svc.filterDate(index, 'quarterly'))



