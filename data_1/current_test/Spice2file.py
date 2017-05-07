#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os 
import re
import copy
import argparse
import numpy as np
from PIL import Image

def Ext(FileName):
    count = 0
    file = open(FileName)#'ibmpg1t1.sol'

    outt = open('1_f','w')

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
                        linetmp  = [line, ]
                    else:
                        if len(linetmp) > 2:
                            outt.write(','.join(linetmp) + '\n')
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

    print('1...')
    outt.close()
    print('close 1...')
    output = open('1_max', 'w')
    maxtmp = [str(i) for i in recmax]
    output.write(','.join(maxtmp) + '\n')
    print('2...')
    output.close()
    print('finished~')

def GetFloatList(list):
    newlist = copy.deepcopy(list)
    for i in xrange(len(list)):
        newlist[i] = float(list[i]) * 255
    return newlist

def RtC():
    line = open('1_f').readline().strip().split(',')
    SamNum = len(line) - 2
    print('sample num success...')
    print(SamNum)
    #exit(0)

    file = open('1_s_41', 'w')
    for i in xrange(50000):#xrange(SamNum):
        j = i + 50000
        print(j)
        sample = []

        #filef = open('1_f')
        #count = 0
        #while 1:
        #    lines = filef.readlines(10000)
        #    print(len(lines))
        #    if not lines:
        #        break
        #    for line in lines:
        #        ft = line.strip().split(',')[i + 2]
        #        sample.append(ft)
        #        count = count + 1
                #print(count)
        
        for line in open('1_f'):
            line = line.strip().split(',')
            ft = line[j + 2]
            sample.append(ft)
            #count = count + 1
            #print(str(count) + ':' + str(len(line)))
            #print(count)
        #raw_input(len(sample))
        file.write(','.join(sample) + '\n')
    file.close()


def I1J():
    ### For the first 50,000 samples
    ### Max is different for every place
    recmax = open('1_max').readline().strip().split(',')
    recmax = GetFloatList(recmax)
    #print(count)
    count_jpg = 0
    path = 'ibm1jpg4'
    if not os.path.exists(path):
    	os.makedirs(path)

    for line in open('1_s_4'):
        pathtmp = path + os.sep + str(count_jpg) + '.jpg'
        line = line.strip().split(',')
        linetmp = GetFloatList(line)
        Image.open('ibm11.jpg').save(pathtmp)
        imtmp = Image.open(pathtmp)
        sizetmp = imtmp.size
        pxtmp = imtmp.load()
        for j in xrange(sizetmp[0]):
            pxtmp[j,0] = int(linetmp[j]*255/recmax[j])
        count_jpg = count_jpg + 1
        print(count_jpg)

def I1J41():
    ### For the last 50,000 samples
    ### Max is different for every place
    recmax = open('1_max').readline().strip().split(',')
    recmax = GetFloatList(recmax)
    #print(count)
    count_jpg = 0
    path = 'ibm1jpg41'
    if not os.path.exists(path):
    	os.makedirs(path)

    for line in open('1_s_41'):
        pathtmp = path + os.sep + str(count_jpg) + '.jpg'
        line = line.strip().split(',')
        linetmp = GetFloatList(line)
        Image.open('ibm11.jpg').save(pathtmp)
        imtmp = Image.open(pathtmp)
        sizetmp = imtmp.size
        pxtmp = imtmp.load()
        for j in xrange(sizetmp[0]):
            pxtmp[j,0] = int(linetmp[j]*255/recmax[j])
        count_jpg = count_jpg + 1
        print(count_jpg)

def I1J2():

    ### For all 100,000 samples
    ### Max is only one value for all data
    recmax = open('1_max').readline().strip().split(',')
    #recmax = GetFloatList(recmax)
    recmax = np.array(recmax, dtype = 'f')
    elemax = np.amax(recmax)
    #print(count)
    count_jpg = 0
    trainpath = 'ibm1jpg2train'
    testpath = 'ibm1jpg2test'
    if not os.path.exists(trainpath):
    	os.makedirs(trainpath)

    if not os.path.exists(testpath):
    	os.makedirs(testpath)
    
	### For first 50,000 samples
    for line in open('1_s_4'):
        pathtmp = trainpath + os.sep + str(count_jpg) + '.jpg'
        line = line.strip().split(',')
        linetmp = np.array(line, dtype = 'f')
        Image.open('ibm11.jpg').save(pathtmp)
        imtmp = Image.open(pathtmp)
        sizetmp = imtmp.size
        pxtmp = imtmp.load()
        for j in xrange(sizetmp[0]):
            pxtmp[j,0] = int(np.around(linetmp[j]*255/elemax))
        count_jpg = count_jpg + 1
        print(count_jpg)
    ### For last 50,000 samples        
    for line in open('1_s_41'):
        pathtmp = testpath + os.sep + str(count_jpg) + '.jpg'
        line = line.strip().split(',')
        linetmp = np.array(line, dtype = 'f')
        Image.open('ibm11.jpg').save(pathtmp)
        imtmp = Image.open(pathtmp)
        sizetmp = imtmp.size
        pxtmp = imtmp.load()
        for j in xrange(sizetmp[0]):
            pxtmp[j,0] = int(np.around(linetmp[j]*255/elemax))
        count_jpg = count_jpg + 1
        print(count_jpg)

parser = argparse.ArgumentParser(description='Get the original file\'s folder')
parser.add_argument("-f","--FileFolder", type=str,
                    help="directory for samples",
                    default = '../SourceData')

args = parser.parse_args()
FPath = args.FileFolder
FNames = [ path.join(FPath,f) for f in listdir(FPath) if path.isfile(path.join(FPath,f)) and f.strip().split('.')[-1]=='sol']
for filename in FNames:
    Ext(FileName=filename)


