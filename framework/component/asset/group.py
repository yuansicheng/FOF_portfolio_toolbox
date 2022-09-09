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
        return list(self._child_group.values())

    def getChildAsset(self):
        return list(self._child_asset.values())

    def addChildGroup(self, group):
        assert group not in self._child_group
        self._child_group[group.getName()] = group

    def addChildAsset(self, asset):
        assert asset not in self._child_asset
        self._child_asset[asset.getName()] = asset

    def getAllGroup(self):
        # dfs
        all_group = [self]
        for group in self.getChildGroup():
            all_group += group.getAllGroup()
        return all_group

    def getAllAsset(self):
        # dfs
        all_asset = self.getChildAsset()
        for group in self.getChildGroup():
            all_asset += group.getAllAsset()
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