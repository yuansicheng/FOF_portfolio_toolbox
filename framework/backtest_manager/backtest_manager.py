#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author    :   yuansc
# @Contact   :   yuansicheng@ihep.ac.cn
# @Date      :   2022-09-26

import os, sys, logging
from datetime import datetime
from tqdm import tqdm

framework_path = os.path.join(os.path.dirname(__file__), '..')
if framework_path not in sys.path:
    sys.path.append(framework_path)

from import_func import getSvc
from component.order_manager.order_manager import OrderManager

date_svc = getSvc('DateSvc')

class BackTestManager:
    def __init__(self, strategy, args={}) -> None:
        logging.info('init BackTestManager')
        self._strategy = strategy
        self._order_manager = OrderManager()

        self._dataset = None
        self._orders = []
        self._weights = {}

        self.setBacktestName()
        self._setArgs(args)
        self._setDateIndex()
        self._setStrategyInitCash()

    def setBacktestName(self, name='backtest'):
        self._name = name

    def _setArgs(self, args):
        # init args
        self._args = {
            'date_range': [[2010, 1, 1], [2010, 12, 31]], 
            'frequency': 'monthly', 
            'cash': 1e4, 
        }

        # set args
        self._args.update(args)

        # add properties
        for k, v in self._args.items():
            setattr(self, k, v)

        # convert date_range to datetime
        self.date_range = [datetime(d[0], d[1], d[2]) for d in self.date_range]

    def _setDateIndex(self):
        # set date_index for backtest
        self._date_index = date_svc.getIndex(self.date_range[0], self.date_range[1])
        # which date to run strategy
        self._run_strategy_date_index = date_svc.filterDateIndex(self._date_index, frequency=self.frequency)

    def _setStrategyInitCash(self):
        self._strategy.setInitCash(self.cash)

    def _executeOrders(self):
        pass

    def _updateAfterClose(self):
        pass

    def _updateAfterExecuteOrders(self):
        pass

    def _weights2Orders(self):
        pass

    def getDataset(self):
        return self._dataset

    def getOrderManager(self):
        return self._order_manager

    def backtest(self):
        # loop date index
        for id_date in tqdm(
            self._date_index, 
            desc = 'backtest', 
            unit = 'days', 
            ):
            logging.debug('backtest: '.format(id_date))

            # 1. run strategy
            self._dataset, self._weights, self._orders = self._strategy.run(id_date)

            # 2. convert weights to orders
            self._weights2Orders()

            # 3. update daily returns and nav
            self._updateAfterClose()

            # 4. execute orders
            self._executeOrders()

            # 5. update return rate and weight
            self._updateAfterExecuteOrders()

# test
from svc.raw_data_svc.lxw_winddb_raw_data_svc.lxw_winddb_raw_data_svc import LxwWinddbRawDataSvc as RawDataSvc
raw_data_svc = RawDataSvc()
date_svc.setTradeDays(raw_data_svc.getTradeDays())

strategy = object()
btm = BackTestManager(strategy, {})
btm.backtest()


        