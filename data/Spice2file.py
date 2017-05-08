#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import listdir, path, makedirs
import re
import copy
import argparse
import numpy as np
from PIL import Image

def Ext(FileName):
    count = 0
    file = open(FileName)#'ibmpg1t1.sol'

    outt = []###open('1_f','w')

    recmax = []

    while 1:
        lines = file.readlines(100000)
        if not lines:
            break
        for line in lines:   
            line = line.strip()
            if len(line) > 0:
                if not re.match(r'^[\-]?\d',line):
                    if not re.match(r'^END', line):
                        ###linetmp  = [line, ]
                        linetmp  = []
                    else:
                        if len(linetmp) > 2:
                            ###outt.write(','.join(linetmp) + '\n')
                            outt.append(linetmp)
                            linetmp  = []
                            count = count + 1
                            print(count)
                else: 
                    numtmp = float(line)
                    #print(numtmp)
                    if numtmp > 0.9:
                        numtmp = 1.8 - numtmp
                        if numtmp < 0:
                            numtmp = 0
                        #print(numtmp)                 
                        linetmp.append(str(numtmp))
                    
                        if len(recmax) < count + 1:
                            recmax.append(numtmp)
                        else:
                            if recmax[-1] < numtmp:
                                recmax[-1] = numtmp

    return outt

parser = argparse.ArgumentParser(description='Get the original file\'s folder')
parser.add_argument("-f","--FileFolder", type=str,
                    help="directory for samples",
                    default = '../../SourceData')

args = parser.parse_args()
FPath = args.FileFolder
FNames = [ path.join(FPath,f) for f in listdir(FPath) if path.isfile(path.join(FPath,f)) and f.strip().split('.')[-1]=='sol']
for filename in FNames:
    print(filename)
    node_time_list = Ext(FileName=filename)
    #node_time_array = np.asarray(node_time_list)
    print('Read in original file finished!')
    time_node_array = np.transpose(node_time_list)
    print('Transpose finished!')
    max_value = np.amax(time_node_array)
    print('Maximum:' + str(max_value))

    tmpdir = path.basename(filename).split('.')[-2]
    if not path.exists(tmpdir):
        makedirs(tmpdir)
    np.save(path.join(tmpdir, 'time_node_array.npy'), time_node_array)

    rtmpdirtr = path.join(tmpdir, 'rtrain')
    if not path.exists(rtmpdirtr):
        makedirs(rtmpdirtr)
    rtmpdirte = path.join(tmpdir, 'rtest')
    if not path.exists(rtmpdirte):
        makedirs(rtmpdirte)
    
    stmpdirtr = path.join(tmpdir, 'strain')
    if not path.exists(stmpdirtr):
        makedirs(stmpdirtr)
    stmpdirte = path.join(tmpdir, 'stest')
    if not path.exists(stmpdirte):
        makedirs(stmpdirte)

    i = 0
    for line in time_node_array:
        #line = line.strip().split(',')
        #line = np.array(line)
        #line = line.astype(np.float)
        print(line)
        line1 = line*255.0/max_value
        print(line1)
        linemin = np.amin(line1)
        linemax = np.amax(line1)
        #if linemax > 200:
        print(str(i) + ': min- ' + str(linemin) + ' max- ' + str(linemax))
        line3 = line1.astype(np.uint8)
        linemin = np.amin(line3)
        linemax = np.amax(line3)
        print(str(i) + ': min- ' + str(linemin) + ' max- ' + str(linemax))

        line3 = np.reshape(line3, (2,541))
        im = Image.fromarray(line3)
        ### randomly divide data into train and test datasets
        seed = np.random.random()
        if seed < 0.5:
            im.save(path.join(rtmpdirtr, str(i) + '.png'))
        else:
            im.save(path.join(rtmpdirte, str(i) + '.png'))
        ### sequentially divide data into train and test datasets
        if i%2 < 1:
            im.save(path.join(stmpdirtr, str(i) + '.png'))
        else:
            im.save(path.join(stmpdirte, str(i) + '.png'))
        
        i = i + 1
    print('Pics for ' + tmpdir + ' finished!')


