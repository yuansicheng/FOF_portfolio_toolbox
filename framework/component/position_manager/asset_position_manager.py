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
    '''
    资产仓位管理器
    做多/做空，保证金比率
    适用普通资产/基金/期货
    '''
    def __init__(self) -> None:
        super().__init__()

        # buy and sell
        self._transection_rate = [0., 0.]

        # 保证金比率，杠杆率=1/保证金比率
        self.addPositionData('margin_ratio', init_value=1)
        # 当前状态：0:无、1:多头、-1:空头
        self.addPositionData('status', init_value=0)

    def setTransectionRate(self, transection_rate):
        if isinstance(transection_rate, (int, float)):
            transection_rate = [transection_rate] * 2
        self._transection_rate = transection_rate

    def setMarginRatio(self, margin_ratio):
        self.margin_ratio = margin_ratio
        
    def updateAfterClose(self, nav):
        # 每日收盘后, 计算资产当天收益并加入仓位中
        self.nav = nav
        self.updateReturns()

    def updateAfterExecuteOrders(self):
        # 执行订单后, 更新收益率
        self.updateReturns()

    def updateReturns(self):
        self.position = self.nav * self.shares
        self.holding_return = self.shares * (self.nav - self.cost_per_unit)
        self.truth_position = self.margin + self.holding_return
        self.holding_yield = self.holding_return / self.investment if self.investment else 0
        self.total_return = self.holding_return + self.historical_return

    def executeOrder(self, order) -> float:
        '''
        input: an order
        '''
        if order.option == 'clear_all':
            self._clearAll(order)
        elif order.option == 'buy':
            if self.status == 0:
                self._open(order)
            else:
                self._buy(order)
        elif order.option == 'sell':
            self._sell(order)
        else:
            logging.error('Order Ececuted Error')

    def _open(self, order):
        '''
        开仓，先设置状态，再买入
        '''
        self.status = order.direction
        self._buy(order)

    def _buy(self, order):
        '''
        买入资产
        1、投资增加
        2、扣除交易成本
        3、计算买入份额
        4、保证金增加
        5、计算持仓成本
        '''
        order.shares_before = self.shares
        # 1        
        self.investment += order.buy_money
        # 2
        cost = order.buy_money * self._transection_rate[0]
        self.transection_cost += cost
        # 3
        buy_shares = ((order.buy_money / self.nav) * (1 - self._transection_rate[0]) * self.status) / self.margin_ratio
        # 4
        self.margin += order.buy_money - cost
        # 5
        if not self.shares:
            self.cost_per_unit = self.nav
        else:
            self.cost_per_unit = abs(self.shares*self.cost_per_unit + buy_shares*self.nav) / abs(self.shares + buy_shares) 
        self.shares += buy_shares

        order.executed = 1
        order.delta_cash = -order.buy_money
        order.transection_cost = cost
        order.shares_after = self.shares


    def _sell(self, order):
        '''
        卖出资产
        1、投资减少
        2、保证金减少
        3、份额减少
        4、扣除交易成本 
        5、历史收益增加      
        '''
        order.shares_before = self.shares
        # 1
        self.investment *= (1 - order.sell_proportion)
        # 2
        self.margin *= (1 - order.sell_proportion)
        # 3
        sell_shares = self.shares * order.sell_proportion
        self.shares -= sell_shares
        # 4
        cost = self.nav * sell_shares * self._transection_rate[1]
        self.transection_cost += cost
        # 5 
        self.historical_return += self.holding_return * order.sell_proportion

        order.executed = 1
        order.delta_cash = self.margin * order.sell_proportion + self.holding_return * order.sell_proportion - cost
        order.transection_cost = cost
        order.shares_after = self.shares
        

    def _clearAll(self, order):
        # logging.debug('clear all')
        self.status = 0
        order.sell_proportion = 1
        return self._sell(order)

# # test
# apm = AssetPositionManager()
# print(apm.getHistoricalData())

    