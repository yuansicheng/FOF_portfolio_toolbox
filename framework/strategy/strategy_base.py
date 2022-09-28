#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author    :   yuansc
# @Contact   :   yuansicheng@ihep.ac.cn
# @Date      :   2022-09-26

import os, sys, logging

framework_path = os.path.join(os.path.dirname(__file__), '..')
if framework_path not in sys.path:
    sys.path.append(framework_path)

from alg.alg_base import AlgBase

from component.asset.group import Group
from component.asset.cash_asset import CashAsset

from component.position_manager.cash_position_manager import CashPositionManager


class StrategyBase(AlgBase):
    '''
    strategy can be interpreted as a pipeline of alg
    '''

    def __init__(self, name, args={}) -> None:
        super().__init__(name)
        self._initAlgDict()

        self._dataset = None
        # init dataset
        self._initDataset()

    def setArgsForAlgs(self, args):
        assert isinstance(args, dict)
        for alg_name, alg in self._alg_dict.items():
            if alg_name in args:
                alg.setArgs(args[alg_name])

    def _initAlgDict(self, alg_dict={}):
        self._alg_dict = alg_dict

    def _initDataset(self):
        # init root group
        self._dataset = Group('root')

        # add cash asset
        cash_asset = CashAsset()
        cash_asset.setPositionManager(CashPositionManager())
        self._dataset.addChildAsset(cash_asset)

    def setInitCash(self, init_cash):
        self.getDataset().getAsset('cash').updateCash(init_cash)

    def getDataset(self):
        return self._dataset

    def run(self, id_date):
        raise NotImplementedError

# # test
# strategy = StrategyBase('test', {})
# # strategy.getDataset().print()
# strategy.setInitCash(1e4)
# print(strategy.getDataset().getAsset('cash').getPositionManager().position)
