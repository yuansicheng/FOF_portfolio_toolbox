#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-29 

import os, sys, argparse, logging

import quantstats as qs
import quantstats.utils as _utils
qs.extend_pandas()

import numpy as np
import pandas as pd

svc_path = os.path.join(os.path.dirname(__file__), '..')
if svc_path not in sys.path:
    sys.path.append(svc_path)

from import_svc import getSvc
constant_svc = getSvc('ConstantSvc')

svc_path = os.path.join(os.path.dirname(__file__), '..')
if svc_path not in sys.path:
    sys.path.append(svc_path)

from singleton import Singleton

class IndicatorSvc(Singleton):
    def __init__(self, ) -> None:
        if not self._isFirstInit():
            return
        print('init IndicatorSvc')

    def getReturn(self, data, periods=constant_svc.DAY_OF_YEAR, annualize=True, prepare_returns=True):
        data = data.fillna(method='ffill').dropna()
        assert data.shape[0], 'cannot handle null data'
        if prepare_returns:
            return_ = data[-1] / data[0]
        else:
            return_ = data.cumprod()[-1]
        # print(return_)
        if annualize:
            return return_ ** (periods/data.shape[0]) - 1
        return return_ - 1

    def getVolatility(self, data, periods=constant_svc.DAY_OF_YEAR, annualize=True, prepare_returns=True):
        return qs.stats.volatility(data, periods=periods, annualize=annualize, prepare_returns=prepare_returns)

    def getSharpe(self, data, rf=constant_svc.RISK_FREE, periods=252, annualize=True, smart=False):
        return qs.stats.sharpe(data, rf=rf, periods=periods, annualize=annualize, smart=smart)

    def getSortino(self, data, rf=constant_svc.RISK_FREE, periods=252, annualize=True, smart=False):
        return qs.stats.sortino(data, rf=rf, periods=periods, annualize=annualize, smart=smart)

    def getCalmar(self, data, prepare_returns=True):
        return qs.stats.calmar(data, prepare_returns=prepare_returns)
    


# test
# data = pd.Series(np.arange(1, 1.51, 0.001)[:100], index =pd.date_range('2020-01-01', periods=100))
# print(data)
# is_ = IndicatorSvc()
# print(is_.getReturn(data))
            

    

    