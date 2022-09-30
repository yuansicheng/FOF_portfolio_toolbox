#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-09-27 

import os, sys, argparse, logging

this_path = os.path.dirname(__file__)
if this_path not in sys.path:
    sys.path.append(this_path)

framework_path = os.path.join(os.path.dirname(__file__), '../..')
if this_path not in sys.path:
    sys.path.append(this_path)

from asset import Asset
from import_func import getSvc

constant_svc = getSvc('ConstantSvc')

class CashAsset(Asset):
    def __init__(self) -> None:
        super().__init__('cash')

        # convert annualize return to daily
        self._daily_yield = (1 + constant_svc.RISK_FREE) ** (1 / constant_svc.DAY_OF_YEAR) - 1

    def updateCash(self, delta_cash):
        assert self.getPositionManager()
        self.getPositionManager().updateCash(delta_cash, transection_cost=self._transection_cost)

    def updateAfterClose(self):
        assert self.getPositionManager() 
        self.getPositionManager().updateAfterClose(self._daily_yield)

    def setIdDate(self, id_date, *args):
        self._id_date = id_date
    
    # cash is always tradable
    def isTradable(self, id_date):
        return True

    def isDelisted(self, id_date):
        return False

# # test
# ca = CashAsset()
# print(ca._daily_yield)
