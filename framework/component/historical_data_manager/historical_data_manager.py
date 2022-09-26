#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-09-09 

import os, sys, argparse, logging

import pandas as pd
import numpy as np
import warnings

class HistoricalDataManager:
    def __init__(self) -> None:
        self._historical_data = pd.DataFrame()

    def addColumn(self, column):
        self._historical_data[column] = np.nan

    def addData(self, data, index=None, column=None):
        if index and column:
            self._historical_data.loc[index, column] = data
        elif index:
            self._historical_data.loc[index] = data
        else:
            i = self._historical_data.shape[0]
            while i in self._historical_data.index:
                i += 1
            self._historical_data.loc[i] = data

    def getAllData(self):
        return self._historical_data

    def getData(self, index=None, column=None):
        if not index and not column:
            return self.getAllData()
        elif index:
            return self.getAllData().loc[index]
        elif column:
            return self.getAllData()[column]
        else:
            return self.getAllData().loc[index, column]
