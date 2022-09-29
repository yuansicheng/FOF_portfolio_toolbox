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

        self._child_group = {}
        self._child_asset = {}  

    def print(self, level=0):
        print('{}group: {}'.format('\t'*level, self._name))
        for asset in self._child_asset.values():
            asset.print(level+1)
        for group in self._child_group.values():
            group.print(level+1)

    def getChildGroup(self):
        return self._child_group

    def getChildAsset(self):
        return self._child_asset

    def addChildGroup(self, group):
        assert group.getName() not in self._child_group
        self._child_group[group.getName()] = group

    def addChildAsset(self, asset):
        assert asset.getName() not in self._child_asset
        self._child_asset[asset.getName()] = asset

    def _updatePreffix(self, preffix, s):
        if not preffix:
            return s
        return preffix + '/' + s

    def getAllGroup(self, is_top=True, preffix=''):
        # dfs
        all_group = {}
        if is_top:
            all_group[self.getName()] = self
        for group in self.getChildGroup().values():
            key = self._updatePreffix(preffix, group.getName())
            all_group[key] = group
            all_group.update(group.getAllGroup(is_top=False, preffix=key))
        return all_group

    def getAllAsset(self, preffix='', ignore_cash=False, id_date=None):
        # dfs
        all_asset = {self._updatePreffix(preffix, name): asset for name, asset in self.getChildAsset().items()}
        for group in self.getChildGroup().values():
            all_asset.update(group.getAllAsset(self._updatePreffix(preffix, group.getName())))
        if ignore_cash and 'cash' in all_asset:
            all_asset.pop('cash')
        if id_date:
            all_asset = {asset: asset_obj for asset, asset_obj in all_asset.items() if asset_obj.isTradable(id_date)}
        return all_asset

    def getGroup(self, group_path):
        if not group_path:
            return self
        if isinstance(group_path, str):
            group_path = group_path.split('/')
        tmp = self._child_group[group_path[0]]
        if len(group_path) == 1:            
            return tmp
        else:
            return tmp.getGroup(group_path[1:])


    def getAsset(self, asset_path):
        if isinstance(asset_path, str):
            asset_path = asset_path.split('/')
        if not asset_path:
            return None
        return self.getGroup(asset_path[:-1])._child_asset[asset_path[-1]]

    def setIdDateRecursively(self, id_date, *args):
        for group in self.getAllGroup().values():
            group.setIdDate(id_date)
        for asset in self.getAllAsset().values():
            asset.setIdDate(id_date, *args)

    def updateAfterCloseRecursively(self):        
        for asset in self.getAllAsset().values():
            asset.updateAfterClose()
        for group in self.getAllGroup().values():
            group.updateAfterClose()

        self.updateWeightRecursively()

    def updateAfterExecuteOrdersRecursively(self):
        for asset in self.getAllAsset().values():
            asset.updateAfterExecuteOrders()
        for group in self.getAllGroup().values():
            group.updateAfterExecuteOrders()

        self.updateWeightRecursively()

    def updateWeightRecursively(self):
        total = self.getPositionManager().position
        for asset in self.getAllAsset().values():
            asset.updateWeight(total)
        for group in self.getAllGroup().values():
            group.updateWeight(total)

    def updateAfterClose(self):
        assert not self.getPositionManager() is None
        self.getPositionManager().updateAfterClose(self.getAllAsset())

    def updateAfterExecuteOrders(self):
        assert not self.getPositionManager() is None
        self.getPositionManager().updateAfterExecuteOrders(self.getAllAsset())

        





# # test
# root = Group('root')
# g1 = Group('g1')
# g2 = Group('g2')
# root.addChildGroup(g1)
# g1.addChildGroup(g2)

# from asset import Asset
# root.addChildAsset(Asset('a1'))
# g1.addChildAsset(Asset('a2'))
# g2.addChildAsset(Asset('a3'))

# root.print()
# print(root.getGroup('g1/g2').getName())
# print(root.getAsset('g1/a2').getName())

# print(root.getAllGroup())
# print(root.getAllAsset())