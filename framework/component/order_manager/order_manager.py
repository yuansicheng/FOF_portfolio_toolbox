#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author    :   yuansc
# @Contact   :   yuansicheng@ihep.ac.cn
# @Date      :   2022-09-24

import os, sys, logging

component_path = os.path.join(os.path.dirname(__file__), '..')
if component_path not in sys.path:
    sys.path.append(component_path)

this_path = os.path.dirname(__file__)
if this_path not in sys.path:
    sys.path.append(this_path)

from historical_data_manager.historical_data_manager import HistoricalDataManager

from order import Order

class OrderManager:
    def __init__(self) -> None:
        self._historical_data_manager = HistoricalDataManager()
        self._columns = Order(date='dummy', asset='dummy', clear_all=1)._columns
        for column in self._columns:
            self._historical_data_manager.addColumn(column)

        self._index = 0

    def getAllOrders(self):
        return self._historical_data_manager.getAllData()

    def addOrder(self, order):
        order_data = [getattr(order, column) for column in self._columns]
        self._historical_data_manager.addData(order_data, index=self._index)

        self._index += 1
        

