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
from component.order_manager.order import Order

from copy import deepcopy

date_svc = getSvc('DateSvc')

class BackTestManager:
    def __init__(self, strategy, name='backtest', args={}) -> None:
        logging.info('init BackTestManager')
        self._strategy = strategy
        self._dataset = self._strategy.getDataset()
        self._name = name
        self._order_manager = OrderManager()

        self._orders = []
        self._weights = {}

        self._setArgs(args)
        self._setDateIndex()
        self._setStrategyInitCash()

        self._id_date = None


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
        logging.info('setting date index')
        # set date_index for backtest
        self._date_index = date_svc.getIndex(self.date_range[0], self.date_range[1])
        # which date to run strategy
        self._run_strategy_date_index = date_svc.filterDateIndex(self._date_index, frequency=self.frequency)

    def _setStrategyInitCash(self):
        logging.info('setting init cash')
        self._strategy.setInitCash(self.cash)

    def _executeOrders(self):
        logging.debug(self.getDataset().getAsset('cash').getPositionManager().position)
        for order in self._orders:
            # print('order before')
            # order.print()
            self.getDataset().getAsset(order.asset).executeOrder(order)
            self.getDataset().getAsset('cash').updateCash(order.delta_cash)
            self.getOrderManager().addOrder(order)
            # print('order after')
            # order.print()
            logging.debug((order.asset, order.option, order.delta_cash))
            logging.debug(self.getDataset().getAsset('cash').getPositionManager().position)


        # clear orders and weights
        self._orders = []
        self._weights = {}


    def _updateAfterClose(self):
        self.getDataset().updateAfterCloseRecursively()

    def _updateAfterExecuteOrders(self):
        self.getDataset().updateAfterExecuteOrdersRecursively()

    def _weights2Orders(self):
        # add asset which not assigned
        if self._weights:
            self._weights.update({asset: 0 for asset in self.getDataset().getAllAsset(ignore_cash=True, id_date=self._id_date) if asset not in self._weights})
        # convert weights to orders
        open_flag = False
        for asset, weight in self._weights.items():
            target_position = self.getDataset().getPositionManager().truth_position * weight
            asset_obj = self._getAssetObj(asset)
            asset_position_manager = asset_obj.getPositionManager()
            tmp_order = Order(
                date = self._id_date, 
                asset = asset, 
            )
            # clear_all
            if ((not weight) and asset_position_manager.position) or asset_position_manager.position * target_position < 0:
                tmp_order_clear_all = deepcopy(tmp_order)
                tmp_order_clear_all.option = 'clear_all'
                self._orders.append(tmp_order_clear_all)
                if not weight:
                    continue
                else:
                    open_flag = True

            tmp_order.target_position = target_position
            # open
            if not asset_position_manager.status or open_flag:
                tmp_order.option = 'open'               
                open_flag = False

            # buy
            elif abs(target_position) >= abs(asset_position_manager.position):
                tmp_order.option = 'buy'
            # sell
            else:
                tmp_order.option = 'sell'
                if not asset_position_manager.status:
                    continue

            self._orders.append(tmp_order)
            

    def _addOrdersForDelistedAssets(self):
        # if delisted, then clear all
        delisted_assets = {asset: asset_obj for asset, asset_obj in self.getDataset().getAllAsset().items() if asset_obj.isDelisted(self._id_date) and self._getAssetObj(asset).getPositionManager().position}

        for asset in delisted_assets:
            self._orders.append(Order(
                date = self._id_date, 
                asset = asset, 
                clear_all = 1 
            ))

    def _getAssetObj(self, asset):
        return self.getDataset().getAsset(asset)

    def getDataset(self):
        return self._dataset

    def getOrderManager(self):
        return self._order_manager

    def backtest(self):
        # loop date index
        for self._id_date in tqdm(
            self._date_index, 
            desc = 'backtest', 
            unit = 'days', 
            ):
            logging.debug('backtest: {}'.format(self._id_date))

            # 1. update daily returns and nav
            self._strategy.setIdDate(self._id_date)
            # logging.debug('{}, update after close'.format(self._id_date)) 
            self._updateAfterClose()

            # 2. run strategy
            if self._id_date in self._run_strategy_date_index:
                # logging.debug('{}, run strategy'.format(self._id_date))
                self._weights, self._orders = self._strategy.run(self._id_date)

                # update dataset, beacuse strategy has authority to add asset
                self._dataset = self._strategy.getDataset()

                # 3. convert weights to orders
                # logging.debug('{}, convert orders'.format(self._id_date))
                self._weights2Orders()
                self._addOrdersForDelistedAssets()

                # 4. execute orders
                # logging.debug('{}, execute orders'.format(self._id_date))
                self._executeOrders()

            # 5. update return rate and weight
            # logging.debug('{}, update after execute orders'.format(self._id_date))
            self._updateAfterExecuteOrders()

# # test
# from svc.raw_data_svc.lxw_winddb_raw_data_svc.lxw_winddb_raw_data_svc import LxwWinddbRawDataSvc as RawDataSvc
# raw_data_svc = RawDataSvc()
# date_svc.setTradeDays(raw_data_svc.getTradeDays())

# strategy = object()
# btm = BackTestManager(strategy, {})
# btm.backtest()


        