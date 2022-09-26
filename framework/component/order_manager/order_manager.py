#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author    :   yuansc
# @Contact   :   yuansicheng@ihep.ac.cn
# @Date      :   2022-09-24

import os, sys, logging

component_path = os.path.join(os.path.dirname(__file__), '..')
if component_path not in sys.path:
    sys.path.append(component_path)

from historical_data_manager.historical_data_manager import HistoricalDataManager

class OrderManager:
    def __init__(self) -> None:
        self._historical_data_manager = HistoricalDataManager()
        self._columns = [
            'date', 
            'asset', 
            'money',  
            'executed', 
            'execute_money', 
            'clear_all', 
            'orther', 
        ]
        for column in self._columns:
            self._historical_data_manager.addColumn(column)

            self._index = 0

    def getAllOrders(self):
        return self._historical_data_manager.getAllData()

    def addOrder(self, order):
        order_data = [getattr(order, column) for column in self._columns[:-1]]
        # save other columns as a str
        other_columns = [column for column in order._columns if column not in self._columns]
        order_data.append({k:v for k,v in other_columns}.__str__())
        self._historical_data_manager.addData(order_data, index=self._index)

        self._index += 1
        

