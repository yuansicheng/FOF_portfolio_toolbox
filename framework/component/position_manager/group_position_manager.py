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

        self._is_root = False

    def setRoot(self, is_root):
        self._is_root = is_root

    def isRoot(self):
        return self._is_root

    def getAssetSum(self, all_asset, key, abs_=False):
        if not abs_:
            return sum([getattr(asset.getPositionManager(), key) for asset in all_asset.values()])
        else:
            return sum([abs(getattr(asset.getPositionManager(), key)) for asset in all_asset.values()])
        
    def updateAfterClose(self, all_asset):
        last_truth_position = self.truth_position
        self.updateReturns(all_asset)

        # shares donot change, if not shares, init it
        # update nav and position
        if not self.shares:
            logging.debug('init shares: {}'.format(self.truth_position))
            self.shares = self.truth_position

        if self.isRoot():
            self.nav = self.truth_position / self.shares if self.shares else 1
        else:
            # logging.debug(self.truth_position / last_truth_position)
            self.nav  = self.nav * (self.truth_position / last_truth_position) if last_truth_position else 1

        

    def updateAfterExecuteOrders(self, all_asset):
        # nav donot change, use margin to calculate
        new_investment = self.getAssetSum(all_asset, 'investment')
        if not self.isRoot():
            self.shares = self.shares * (new_investment / self.investment) if self.investment else new_investment
        self.investment = new_investment

        self.updateReturns(all_asset)



    def updateReturns(self, all_asset):
        for key in [    
            'position', # 仓位，持有资产的总价值  
            'truth_position', # 真实仓位，可变现资产    
            # 'cost_per_unit', # 单位份额持仓成本     
            'weight', # 权重
            'truth_weight', # 真实权重，可变现资产的权重
            'margin', # 保证金
            'investment', # 投资
            'holding_return', # 持有收益 = 仓位-投资-持有管理费-持有交易成本
            'holding_yield', # 持有收益率 = 持有收益/总投资
            'historical_return', # 历史收益，执行卖出操作后累加
            'total_return', # 总收益
            'transaction_cost', # 交易成本
            # 'nav', # 单位净值
            # 'shares', #持有份额
            ]:
            setattr(self, key, self.getAssetSum(all_asset, key))

            # self.position = self.getAssetSum(all_asset, 'position', abs_=True)


        self.holding_yield = self.holding_return / self.margin if self.margin else 0

        