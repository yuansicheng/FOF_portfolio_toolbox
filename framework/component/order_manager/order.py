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
        for column in self._columns[:3]:
            assert column in kwargs, '{} not set'.format(column)
        for column in self._columns:
            setattr(self, column, np.nan)

        for k, v in kwargs.items():
            if k in self._columns:
                setattr(self, k, v)
        
# test
from datetime import datetime
order = Order(
    date = datetime(2022, 9, 24), 
    asset = 'test_asset', 
    money = 1000, 
)

    