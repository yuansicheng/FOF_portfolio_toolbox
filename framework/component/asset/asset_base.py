#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-29 

import os, sys, argparse, logging

class AssetBase:
    def __init__(self, name) -> None:
        assert name, 'name must not be None'
        self._name = name
        self._child_group = []
        self._child_asset = []    

    def print(self, level=0):
        raise NotImplementedError

    def getChildGroup(self):
        raise NotImplementedError 

    def getChildAsset(self):
        raise NotImplementedError 

    def addChildGroup(self):
        raise NotImplementedError 

    def addChildAsset(self):
        raise NotImplementedError 

    def getName(self):
        return self._name


# # test
# a1 = AssetBase(1)
# a2 = AssetBase(2)
