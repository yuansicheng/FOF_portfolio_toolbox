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

class AssetPositionManager(PositionManagerBase):
    def __init__(self) -> None:
        super().__init__()
        
    def updateAfterClose(self, daily_yield):
        # 每日收盘后, 计算资产当天收益并加入仓位中
        self.position *= (1 + daily_yield)
        self.updateReturns()

    def updateAfterExecuteOrders(self, total):
        # 执行订单后, 更新权重和收益率
        self.updateWeight(total)
        self.updateReturns()

    def executeOrder(self, order, transection_cost=0.0002) -> float:
        '''
        input: an order
        output: a float means how much money you cost, + for buy and - for sell
        '''
        if order == 'clear_all':
            return self._clearAll()
        elif order.money >= 0:
            return self._buy(order.money, transection_cost)
        else:
            return self._sell(-order.money, transection_cost)


    def _buy(self, money, transection_cost):
        '''
        买入资产
        1、计算交易成本, 交易成本 = money * transection_cost
        2、计算仓位,仓位增加 money - 交易成本
        3、计算投资,投资增加 money - 交易成本
        4、返回 money - 交易成本,即执行订单使用的现金
        '''
        # 1
        cost = money * transection_cost
        self.transection_cost += cost
        tmp = money - cost
        # 2
        self.position += tmp
        # 3
        self.investment += tmp
        # 4
        return tmp

    def _sell(self, money, transection_cost):
        '''
        卖出资产
        a、卖出金额小于仓位
            1、计算交易成本, 交易成本 += money * transection_cost
            2、计算投资,投资减少 money / 仓位 * 投资
            3、计算历史收益增加 money / 仓位 * 持有收益 
            4、计算持有收益减少 money / 仓位 * 持有收益  
            5、计算仓位,仓位减少 money                 
            6、返回 money + transection_cost, 即执行订单后到账的现金
        b、卖出金额大于仓位
            tbd
        '''
        if money <= self.position:
            # 1
            cost = money * transection_cost
            self.transection_cost += cost
            
            frac = money / self.investment
            # 2
            self.investment -= frac * self.investment
            # 3
            self.historical_return += frac * self.hodlding_return
            # 4
            self.holding_return -= frac * self.hodlding_return
            # 5
            self.position -= money
            # 6
            return -money
        else:
            raise NotImplementedError

    def _clearAll(self, transection_cost):
        return self._sell(self.position, transection_cost)

# # test
# apm = AssetPositionManager()
# print(apm.getHistoricalData())

    