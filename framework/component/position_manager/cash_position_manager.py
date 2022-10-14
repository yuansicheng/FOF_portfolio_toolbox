#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author    :   yuansc
# @Contact   :   yuansicheng@ihep.ac.cn
# @Date      :   2022-09-21

import os, sys, logging

this_path = os.path.dirname(__file__)
if this_path not in sys.path:
    sys.path.append(this_path)

from asset_position_manager import AssetPositionManager

class CashPositionManager(AssetPositionManager):
    def __init__(self) -> None:
        super().__init__()

    def updateAfterClose(self, daily_yield):
        self.position *= (1 + daily_yield)
        self.updateReturns()

    def updateAfterExecuteOrders(self):
        self.updateReturns()

    def updateReturns(self):
        self.holding_return = self.position - self.investment
        self.truth_position = self.position
        self.holding_yield = self.holding_return / abs(self.investment) if self.investment else 0.
        self.total_return = self.holding_return + self.historical_return

    def updateCash(self, delta_cash):
        if self.position * delta_cash < 0:
            if abs(self.position) >= abs(delta_cash):
                self._reduce(delta_cash)
            else:
                self._clearAll()
                self._add(self.position + delta_cash)
        else:
            self._add(delta_cash)

    def _clearAll(self):
        # logging.debug('clear all')
        return self._reduce(-self.position)

    def _add(self, delta_cash):
        self.position += delta_cash
        self.investment += delta_cash

    def _reduce(self, delta_cash):
        frac = abs(delta_cash / self.position)
        self.investment -= frac * self.investment

        self.holding_return -= frac * self.holding_return
        self.historical_return += frac * self.holding_return

        self.position -= frac * self.position
            


    