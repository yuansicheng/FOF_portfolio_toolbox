#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-09-01 

import os, sys, argparse, logging

asset_path = os.path.dirname(__file__)
if asset_path not in sys.path:
    sys.path.append(asset_path)

from asset_base import AssetBase

class Asset(AssetBase):
    def __init__(self, name) -> None:
        super().__init__(name)

    def print(self, level=0):
        print('{}asset: {}'.format('\t'*level, self._name))

    def getNav(self):
        raise NotImplementedError

# # test
# a = Asset('1')
# a.getChildAsset()