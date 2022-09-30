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
            'money',  
            'executed', 
            'execute_money', 
            'transection_cost', 
            'clear_all', 
            'orther', 
        ]
        for column in self._columns:
            setattr(self, column, np.nan)

        for k, v in kwargs.items():
            if k in self._columns:
                setattr(self, k, v)

        assert self.date
        assert self.asset
        # assert not np.isnan(self.money) or self.clear_all

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

    