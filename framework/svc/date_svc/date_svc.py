#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-12 

import os, sys, argparse, logging

raw_data_svc_path = os.path.join(os.path.dirname(__file__), '../raw_data_svc')
if raw_data_svc_path not in sys.path:
    sys.path.append(raw_data_svc_path)

from sql_raw_data_svc import sql_raw_data_svc

__all__ = ['date_svc']

class DateSvc:
    def __init__(self) -> None:
        print('init date_svc')
        self._sql_raw_data_svc = sql_raw_data_svc
        self.setMode()
        self._setTradeDays()

    def _setTradeDays(self):
        sql = "SELECT TRADE_DAYS FROM asharecalendar WHERE S_INFO_EXCHMARKET='{}' ORDER BY TRADE_DAYS".format(self._mode)
        self._trade_days = self._sql_raw_data_svc.query(sql)['TRADE_DAYS']

    ###########################################
    # api

    def setMode(self, mode='SSE'):
        self._mode = mode
        self._setTradeDays()

    def getAllTradeDays(self):
        return self._trade_days

    def cutDataWithIndex(self, data, index):
        pass

    def cutDataWithWindow(self, id_date, window):
        pass

    def cutDataWithRange(self, start_date, end_date):
        pass

    def formatIndex(self, data):
        pass


date_svc = DateSvc()

# test
# print(date_svc.getAllTradeDays())


