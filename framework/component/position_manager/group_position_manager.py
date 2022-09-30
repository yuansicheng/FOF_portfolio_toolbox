#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author    :   yuansc
# @Contact   :   yuansicheng@ihep.ac.cn
# @Date      :   2022-09-21

import os, sys, logging

this_path = os.path.dirname(__file__)
if this_path not in sys.path:
    sys.path.append(this_path)

from position_manager_base import PositionManagerBase

class GroupPositionManager(PositionManagerBase):
    def __init__(self) -> None:
        super().__init__()

        # 单位净值
        self.addPositionData('nav', 1)
        # 份额
        self.addPositionData('shares', 0)

    def getAssetSum(self, all_asset, key):
       return sum([getattr(asset.getPositionManager(), key) for asset in all_asset.values()])
        
    def updateAfterClose(self, all_asset):
        new_position = self.getAssetSum(all_asset, 'position')

        # shares donot change, if not shares, init it
        # update nav and position
        if not self.shares:
            self.shares = new_position
        self.nav *= new_position / self.position if self.position else self.nav
        self.position = new_position

    def updateAfterExecuteOrders(self, all_asset):
        for key in [           
            'weight', # 权重
            'transection_cost', # 总交易成本
            'investment', # 投资
            'holding_return', # 持有收益 = 仓位-总投资
            'historical_return', # 历史收益，执行卖出操作后累加
            'total_return', # 总收益 = 持有收益 + 历史收益 - 交易成本
            ]:
            setattr(self, key, self.getAssetSum(all_asset, key))

        self.holding_yield = self.holding_return / self.investment if self.investment else 0

        # nav donot change
        new_position = self.getAssetSum(all_asset, 'position')
        self.shares *= new_position / self.position if self.position else new_position
        self.position = new_position

        