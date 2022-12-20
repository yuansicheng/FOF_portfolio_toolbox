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
        self._transaction_rate = [0., 0.]

        # 保证金比率，杠杆率=1/保证金比率
        self.addPositionData('margin_ratio', init_value=1)
        # 当前状态：0:无、1:多头、-1:空头
        self.addPositionData('status', init_value=0)

    def settransactionRate(self, transaction_rate):
        if isinstance(transaction_rate, (int, float)):
            transaction_rate = [transaction_rate] * 2
        self._transaction_rate = transaction_rate

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
        # logging.debug(self.shares * (self.nav - self.cost_per_unit) - self.holding_return)
        self.holding_return = self.shares * (self.nav - self.cost_per_unit)
        self.truth_position = self.margin + self.holding_return
        self.holding_yield = self.holding_return / self.investment if self.investment else 0
        self.total_return = self.holding_return + self.historical_return

    def executeOrder(self, order) -> float:
        '''
        input: an order
        '''
        if order.option == 'clear_all':
            order.target_position = 0
            self._clearAll(order)
        elif order.option =='open':
            self._open(order)
        elif order.option == 'buy':
            if self.status == 0:
                self._open(order)
            else:
                self._buy(order)
        elif order.option == 'sell':
            self._sell(order)
        else:
            logging.error('Order Ececuted Error')

    def _updateMargin(self):
        if self.status >= 0 and self.margin_ratio==1:
            return 0
        target_margin = self.position * self.margin_ratio * self.status
        delta_margin = target_margin - self.margin
        self.investment += delta_margin

        self.margin = target_margin

        return -delta_margin

    def _open(self, order):
        '''
        开仓，先设置状态，再买入
        '''
        if not order.target_position:
            return
        self.status = order.target_position / abs(order.target_position)
        self._buy(order)

    def _buy(self, order):
        '''
        买入资产
        1、投资增加       
        2、计算买入份额
        3、扣除交易成本
        4、保证金增加
        5、计算持仓成本
        '''
        order.shares_before = self.shares  
        delta_cash = self._updateMargin()   
        # 2
        buy_position = order.target_position - self.position
        buy_shares = buy_position / self.nav
        # 3
        cost = buy_position * self._transaction_rate[0]
        self.transaction_cost += cost
        # 4
        delta_margin = buy_position * self.margin_ratio * self.status
        self.margin += delta_margin
        # 5
        if not self.shares:
            self.cost_per_unit = self.nav
        else:
            self.cost_per_unit = abs(self.shares*self.cost_per_unit + buy_shares*self.nav) / abs(self.shares + buy_shares) 
        self.shares += buy_shares

        # 1  
        delta_cash += (-delta_margin - cost)      
        self.investment += delta_margin + cost
        self.position = self.shares * self.nav

        order.executed = 1
        order.delta_cash = delta_cash
        order.transaction_cost = cost
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
        delta_cash = self._updateMargin()  
        sell_proportion = 1 - order.target_position / self.position 
        
        # 1
        self.investment *= (1 - sell_proportion)
        # 2
        delta_margin = self.margin * sell_proportion
        self.margin *= (1 - sell_proportion)
        # 3
        sell_shares = self.shares * sell_proportion
        self.shares -= sell_shares
        # 4
        cost = self.nav * sell_shares * self._transaction_rate[1]
        self.transaction_cost += cost
        # 5 
        self.historical_return += self.holding_return * sell_proportion
        self.position = self.shares * self.nav

        delta_cash += (delta_margin + self.holding_return * sell_proportion - cost)

        order.executed = 1
        order.delta_cash = delta_cash
        order.transaction_cost = cost
        order.shares_after = self.shares
        

    def _clearAll(self, order):
        # logging.debug('clear all')
        self.status = 0
        order.sell_proportion = 1
        return self._sell(order)

# # test
# apm = AssetPositionManager()
# print(apm.getHistoricalData())

    