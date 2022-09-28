#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-09-26 

import os, sys, argparse, logging

class AlgBase:
    def __init__(self, name, args=None) -> None:
        self._name = name
        self._args = args

    def getName(self):
        return self._name

    def setArgs(self, args):       
        self._args = args
        for k, v in self._args.items():
            setattr(self, k, v)

    def run(self, *args, **kwargs):
        raise NotImplementedError