#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/1/6 9:06 下午
# @Author  : lance.txl
# @Site    : 
# @File    : utils.py
# @Software: PyCharm

import os

def ergodicDir(Dir, FileType=""):
    fileDict = {}
    for parent, dirnames, filenames in os.walk(Dir):
        for i in filenames:
            if FileType != "":
                if i.split(".", -1)[-1] == FileType:
                    fileDict[os.path.join(parent, i)] = os.path.join(parent, i)
            else:
                fileDict[os.path.join(parent, i)] = os.path.join(parent, i)
    return fileDict

