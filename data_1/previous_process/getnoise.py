#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os 
import copy
import numpy as np

def GetFloatList(list):
    newlist = copy.deepcopy(list)
    for i in xrange(len(list)):
        newlist[i] = float(list[i])
    return newlist

CurrentPath = '.'#os.path.join('.', os.sep())

f = []
for (dirpath, dirnames, filenames) in os.walk(CurrentPath):
    f.extend(filenames)
    break

for file in f:
    appendix = file.split('.')
    ##appendix = appendix[-1]
    if appendix[-1] == 'csv':
        path = appendix[-2]
        if not os.path.exists(path):
            os.mkdir(path)
        Lines = [line.strip().split(',')[1:] for line in open(file)]
        for i in xrange(len(Lines)):
            TmpW = open(path + os.sep + str(i) + '.txt', 'w')
            TmpW.write(''.join(Lines[i]))
            TmpW.close()
exit(0)