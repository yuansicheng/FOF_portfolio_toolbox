#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author    :   yuansc
# @Contact   :   yuansicheng@ihep.ac.cn
# @Date      :   2022-10-15

import os, sys, logging

import pandas as pd

this_path = os.path.dirname(__file__)
if this_path not in sys.path:
    sys.path.append(this_path)

framework_path = os.path.join(os.path.dirname(__file__), '../framework')
if framework_path not in sys.path:
    sys.path.append(framework_path)

# 获取所有基金的基础数据
from merge_fund_raw_data import MergeFundRawDataAlg
# 筛选类别
from select_fund_type import SelectFundTypeAlg
# 按条件筛选
from select_fund_condition import SelectFundConditionAlg
# 风格识别
from fund_style_identification_alg import FundStyleIdentificationAlg

from import_func import getSvc
from strategy.strategy_base import StrategyBase

from component.asset.group import Group
from component.position_manager.group_position_manager import GroupPositionManager

raw_data_svc = getSvc('LxwWinddbRawDataSvc')
date_svc = getSvc('DateSvc')

class TestFofStrategy(StrategyBase):
    def __init__(self, name, args={}) -> None:
        super().__init__(name, args)

    def _initAlgDict(self):
        self._alg_dict['merge_fund_raw_data'] = MergeFundRawDataAlg('merge_fund_raw_data')
        self._alg_dict['select_fund_type'] = SelectFundTypeAlg('select_fund_type')
        self._alg_dict['select_fund_condition'] = SelectFundConditionAlg('select_fund_condition')
        self._alg_dict['fund_style_identification'] = FundStyleIdentificationAlg('fund_style_identification')

    # 设置数据集
    def _initDataset(self):
        # 父类方法初始化数据集并添加cash资产
        super()._initDataset(init_position_manager=True)

        # 添加两个资产组
        bond_group = Group('bond')
        stock_group = Group('stock')

        bond_group.setPositionManager(GroupPositionManager())
        stock_group.setPositionManager(GroupPositionManager())

        self.getDataset().addChildGroup(bond_group)
        self.getDataset().addChildGroup(stock_group)

    def run(self, id_date):
        # 获取所有可交易的基金
        fund_info = self._alg_dict['merge_fund_raw_data'].run(id_date)
        # logging.debug('fund_data: {} {}'.format(fund_info.head(), fund_info.shape))

        ############################################

        # 债券型基金
        bond_fund_info_type = self._alg_dict['select_fund_type'].run(fund_info.copy(), type_='bond')
        # logging.debug('bond_fund_info_type: {} {}'.format(bond_fund_info_type.head(), bond_fund_info_type.shape))
        
        bond_fund_info_condition = self._alg_dict['select_fund_condition'].run(bond_fund_info_type, type_='bond')
        # logging.debug('bond_fund_info_condition: {} {}'.format(bond_fund_info_condition.head(), bond_fund_info_condition.shape))

        bond_fund_style = self._alg_dict['fund_style_identification'].run(id_date, bond_fund_info_condition, type_='bond')

        ############################################

        # 股票型基金
        stock_fund_info_type = self._alg_dict['select_fund_type'].run(fund_info.copy(), type_='stock')
        # logging.debug('stock_fund_info_type: {} {}'.format(stock_fund_info_type.head(), stock_fund_info_type.shape))

        stock_fund_info_condition = self._alg_dict['select_fund_condition'].run(stock_fund_info_type, type_='stock')
        # logging.debug('stock_fund_info_condition: {} {}'.format(stock_fund_info_condition.head(), stock_fund_info_condition.shape))

        stock_fund_style = self._alg_dict['fund_style_identification'].run(id_date, bond_fund_info_condition, type_='stock')

        return bond_fund_style, stock_fund_style




        

    