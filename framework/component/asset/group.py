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

class Group(AssetBase):
    def __init__(self, name) -> None:
        super().__init__(name)

    def print(self, level=0):
        print('{}group: {}'.format('\t'*level, self._name))
        for group in self._child_group:
            group.print(level+1)
        for asset in self._child_asset:
            asset.print(level+1)

    def getChildGroup(self):
        return self._child_group

    def getChildAsset(self):
        return self._child_asset

    def addChildGroup(self, group):
        self._child_group.append(group)

    def addChildAsset(self, asset):
        self._child_asset.append(asset)

    def getAllGroup(self):
        # dfs
        all_group = [self]
        for group in self.getChildGroup():
            all_group += group.getAllGroup()
        return all_group

    def getAllAsset(self):
        # dfs
        all_asset = []
        for group in self.getChildGroup():
            all_asset += group.getAllAsset()
        return all_asset

# # test
# root = Group('root')
# g1 = Group('1')
# g2 = Group('2')
# root.addChildGroup(g1)
# g1.addChildGroup(g2)
# root.print()
# print([group.getName() for group in root.getAllGroup()])