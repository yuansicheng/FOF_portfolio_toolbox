#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author    :   yuansc
# @Contact   :   yuansicheng@ihep.ac.cn
# @Date      :   2022-09-24

import os, sys, logging
import numpy as np

class Order:
    '''
    normal order
    '''
    def __init__(self, **kwargs) -> None:
        self._columns = [
            'date', 
            'asset',
            'option', 
            'target_position', 
            'sell_proportion', 
            'executed', 
            'delta_cash', 
            'transaction_cost', 
            'shares_before', 
            'shares_after', 
        ]
        for column in self._columns:
            setattr(self, column, None)

        for k, v in kwargs.items():
            if k in self._columns:
                setattr(self, k, v)

        assert self.date
        assert self.asset
        if self.option == 'buy':
            assert self.target_position > 0
        if self.option == 'sell':
            assert self.sell_proportion

    def print(self):
        print('this is an order: ')
        for column in self._columns:
            print('\t{}: {}'.format(column, getattr(self, column)))
        
# # test
# from datetime import datetime
# order = Order(
#     date = datetime(2022, 9, 24), 
#     asset = 'test_asset', 
#     money = 1000, 
# )
# order.print()

    