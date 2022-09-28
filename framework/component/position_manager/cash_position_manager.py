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

    def updateCash(self, delta_cash, transection_cost=0):
        if delta_cash >= 0:
            self._buy(delta_cash, transection_cost)
        else:
            self._sell(delta_cash, transection_cost)

    