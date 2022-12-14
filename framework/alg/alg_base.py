#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-09-26 

import os, sys, argparse, logging

class AlgBase:
    def __init__(self, name, args=None) -> None:
        self._name = name
        self.setArgs(args)

    def getName(self):
        return self._name

    def setArgs(self, args): 
        logging.info('alg {}: init args'.format(self.getName()))      
        self._args = args
        if args:
            for k, v in self._args.items():
                setattr(self, k, v)

    def run(self, *args, **kwargs):
        raise NotImplementedError