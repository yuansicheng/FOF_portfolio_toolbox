#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author    :   yuansc
# @Contact   :   yuansicheng@ihep.ac.cn
# @Date      :   2022-10-15

import os, sys, logging

import pandas as pd

framework_path = os.path.join(os.path.dirname(__file__), '../framework')
if framework_path not in sys.path:
    sys.path.append(framework_path)

from import_func import getSvc

class SelectFundConditionAlg():
    def __init__(self, bond_conditions={}, stock_conditions={}) -> None:
        self.bond_conditions = bond_conditions
        self.stock_conditions = stock_conditions

    def run(self, fund_info, type_=None):
        if type_ == 'bond':
            conditions = self.bond_conditions
        if type_ == 'stock':
            conditions = self.stock_conditions

        # print(fund_info)

        for col, condition in conditions.items():
            if condition >= 0:
                fund_info = fund_info.loc[fund_info[col] >= condition]
            if condition < 0:
                fund_info = fund_info.loc[fund_info[col] <=(-1*condition)]
            # print(fund_info)

        # drop duplicate
        fund_info.drop_duplicates(subset=['f_info_windcode'], keep='first', inplace=True)

        fund_info.reset_index(drop=True, inplace=True)

        return fund_info
    
