#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-15 

import os, sys, argparse, logging

class Singleton:
    _instance = None
    _first_init = True

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls,*args,**kwargs)      
        return cls._instance

    def _isFirstInit(self):
        tmp = self.__class__._first_init
        self.__class__._first_init = False
        return tmp

        